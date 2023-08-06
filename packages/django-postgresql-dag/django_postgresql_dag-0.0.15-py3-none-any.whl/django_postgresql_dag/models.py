"""
A class to model hierarchies of objects following Directed Acyclic Graph structure.

The graph traversal queries use Postgresql's recursive CTEs to fetch an entire tree
of related node ids in a single query. These queries also topologically sort the ids
by generation.

Inspired by:
https://www.fusionbox.com/blog/detail/graph-algorithms-in-a-database-recursive-ctes-and-topological-sort-with-postgres/620/
https://github.com/elpaso/django-dag
https://github.com/worsht/django-dag-postgresql
https://github.com/stdbrouw/django-treebeard-dag
"""

from django.apps import apps
from django.db import models, connection
from django.db.models import Case, When
from django.core.exceptions import ValidationError

LIMITING_FK_EDGES_CLAUSE_1 = (
    """AND second.{fk_field_name}_id = %(limiting_fk_edges_instance_id)s"""
)
LIMITING_FK_EDGES_CLAUSE_2 = (
    """AND {relationship_table}.{fk_field_name}_id = %(limiting_fk_edges_instance_id)s"""
)

LIMITING_FK_NODES_CLAUSE_1 = """"""
LIMITING_FK_NODES_CLAUSE_2 = """"""

EXCLUDED_UPWARD_NODES_CLAUSE_1 = """AND second.child_id <> ALL(%(excluded_upward_node_ids)s::int[])"""  # Used for ancestors and upward path
EXCLUDED_UPWARD_NODES_CLAUSE_2 = (
    """AND {relationship_table}.child_id <> ALL(%(excluded_upward_node_ids)s::int[])"""
)

EXCLUDED_DOWNWARD_NODES_CLAUSE_1 = """AND second.parent_id <> ALL(%(excluded_downward_node_ids)s::int[])"""  # Used for descendants and downward path
EXCLUDED_DOWNWARD_NODES_CLAUSE_2 = (
    """AND {relationship_table}.parent_id <> ALL(%(excluded_downward_node_ids)s::int[])"""
)

REQUIRED_UPWARD_NODES_CLAUSE_1 = """"""  # Used for ancestors and upward path
REQUIRED_UPWARD_NODES_CLAUSE_2 = """"""

REQUIRED_DOWNWARD_NODES_CLAUSE_1 = """"""  # Used for descendants and downward path
REQUIRED_DOWNWARD_NODES_CLAUSE_2 = """"""

ANCESTORS_QUERY = """
WITH RECURSIVE traverse(id, depth) AS (
    SELECT first.parent_id, 1
        FROM {relationship_table} AS first
        LEFT OUTER JOIN {relationship_table} AS second
        ON first.parent_id = second.child_id
    WHERE first.child_id = %(id)s
    -- LIMITING_FK_EDGES_CLAUSE_1
    -- EXCLUDED_UPWARD_NODES_CLAUSE_1
    -- REQUIRED_UPWARD_NODES_CLAUSE_1
    {ancestors_clauses_1}
UNION
    SELECT DISTINCT parent_id, traverse.depth + 1
        FROM traverse
        INNER JOIN {relationship_table}
        ON {relationship_table}.child_id = traverse.id
    WHERE 1 = 1
    -- LIMITING_FK_EDGES_CLAUSE_2
    -- EXCLUDED_UPWARD_NODES_CLAUSE_2
    -- REQUIRED_UPWARD_NODES_CLAUSE_2
    {ancestors_clauses_2}
)
SELECT id FROM traverse
GROUP BY id
ORDER BY MAX(depth) DESC, id ASC
"""

DESCENDANTS_QUERY = """
WITH RECURSIVE traverse(id, depth) AS (
    SELECT first.child_id, 1
        FROM {relationship_table} AS first
        LEFT OUTER JOIN {relationship_table} AS second
        ON first.child_id = second.parent_id
    WHERE first.parent_id = %(id)s
    -- LIMITING_FK_EDGES_CLAUSE_1
    -- EXCLUDED_DOWNWARD_NODES_CLAUSE_1
    -- REQUIRED_DOWNWARD_NODES_CLAUSE_1
    {descendants_clauses_1}
UNION
    SELECT DISTINCT child_id, traverse.depth + 1
        FROM traverse
        INNER JOIN {relationship_table}
        ON {relationship_table}.parent_id = traverse.id
    WHERE 1=1
    -- LIMITING_FK_EDGES_CLAUSE_2
    -- EXCLUDED_DOWNWARD_NODES_CLAUSE_2
    -- REQUIRED_DOWNWARD_NODES_CLAUSE_2
    {descendants_clauses_1}
)
SELECT id FROM traverse
GROUP BY id
ORDER BY MAX(depth), id ASC
"""

PATH_LIMITING_FK_EDGES_CLAUSE = (
    """AND first.{fk_field_name}_id = %(limiting_fk_edges_instance_id)s"""
)
PATH_LIMITING_FK_NODES_CLAUSE = """"""

EXCLUDED_UPWARD_PATH_NODES_CLAUSE = (
    """AND second.parent_id <> ALL('{excluded_path_node_ids}'::int[])"""
)
EXCLUDED_DOWNWARD_PATH_NODES_CLAUSE = (
    """AND second.child_id <> ALL('{excluded_path_node_ids}'::int[])"""
)
REQUIRED_UPWARD_PATH_NODES_CLAUSE = (
    """AND second.parent_id = ALL('{required_path_node_ids}'::int[])"""
)
REQUIRED_DOWNWARD_PATH_NODES_CLAUSE = (
    """AND second.child_id = ALL('{required_path_node_ids}'::int[])"""
)

UPWARD_PATH_QUERY = """
WITH RECURSIVE traverse(child_id, parent_id, depth, path) AS (
    SELECT
        first.child_id,
        first.parent_id,
        1 AS depth,
        ARRAY[first.child_id] AS path
        FROM {relationship_table} AS first
    WHERE child_id = %(starting_node)s
UNION ALL
    SELECT
        first.child_id,
        first.parent_id,
        second.depth + 1 AS depth,
        path || first.child_id AS path
        FROM {relationship_table} AS first, traverse AS second
    WHERE first.child_id = second.parent_id
    AND (first.child_id <> ALL(second.path))
    -- PATH_LIMITING_FK_EDGES_CLAUSE
    -- EXCLUDED_UPWARD_PATH_NODES_CLAUSE
    -- REQUIRED_UPWARD_PATH_NODES_CLAUSE
    -- LIMITING_UPWARD_NODES_CLAUSE_1  -- CORRECT?
    {upward_clauses}
    AND second.depth <= %(max_depth)s
)      
SELECT path FROM traverse
    WHERE parent_id = %(ending_node)s
    LIMIT %(max_paths)s;
"""

DOWNWARD_PATH_QUERY = """
WITH RECURSIVE traverse(parent_id, child_id, depth, path) AS (
    SELECT
        first.parent_id,
        first.child_id,
        1 AS depth,
        ARRAY[first.parent_id] AS path
        FROM {relationship_table} AS first
    WHERE parent_id = %(starting_node)s
UNION ALL
    SELECT
        first.parent_id,
        first.child_id,
        second.depth + 1 AS depth,
        path || first.parent_id AS path
        FROM {relationship_table} AS first, traverse AS second
    WHERE first.parent_id = second.child_id
    AND (first.parent_id <> ALL(second.path))
    -- PATH_LIMITING_FK_EDGES_CLAUSE
    -- EXCLUDED_DOWNWARD_PATH_NODES_CLAUSE
    -- REQUIRED_DOWNWARD_PATH_NODES_CLAUSE
    -- LIMITING_DOWNWARD_NODES_CLAUSE_1  -- CORRECT?
    {downward_clauses}
    AND second.depth <= %(max_depth)s
)      
SELECT path FROM traverse
    WHERE child_id = %(ending_node)s
    LIMIT %(max_paths)s;
"""


class NodeNotReachableException(Exception):
    """
    Exception for node distance and path
    """

    pass


def _filter_order(queryset, field_names, values):
    """
    Filters the provided queryset for 'field_name__in values' for each given field_name in [field_names]
    orders results in the same order as provided values

        For instance
            _filter_order(self.__class__.objects, "pk", ids)
        returns a queryset of the current class, with instances where the 'pk' field matches an id in ids

    """
    if not isinstance(field_names, list):
        field_names = [field_names]
    case = []
    for pos, value in enumerate(values):
        when_condition = {field_names[0]: value, "then": pos}
        case.append(When(**when_condition))
    order_by = Case(*case)
    filter_condition = {field_name + "__in": values for field_name in field_names}
    return queryset.filter(**filter_condition).order_by(order_by)


def node_factory(edge_model, children_null=True, base_model=models.Model):
    edge_model_table = edge_model._meta.db_table

    def get_foreign_key_field(instance=None):
        """
        Provided a model instance and model class, checks if the edge model has a ForeignKey
        field to the model for that instance, and then returns the field name and instance id.
        """
        if instance is not None:
            for field in edge_model._meta.get_fields():
                if field.related_model is instance._meta.model:
                    # Return the first field that matches
                    return field.name
        return None

    class Node(base_model):
        children = models.ManyToManyField(
            "self",
            blank=children_null,
            symmetrical=False,
            through=edge_model,
            related_name="parents",
        )

        class Meta:
            abstract = True

        def add_child(self, descendant, **kwargs):
            kwargs.update({"parent": self, "child": descendant})
            disable_check = kwargs.pop("disable_circular_check", False)
            cls = self.children.through(**kwargs)
            return cls.save(disable_circular_check=disable_check)

        def remove_child(self, descendant):
            self.children.through.objects.get(parent=self, child=descendant).delete()

        def add_parent(self, parent, *args, **kwargs):
            return parent.add_child(self, **kwargs)

        def remove_parent(self, parent):
            parent.children.through.objects.get(parent=parent, child=self).delete()

        def filter_order_ids(self, ids):
            """
            Generates a queryset, based on the current class and the provided ids
            """
            return _filter_order(self.__class__.objects, "pk", ids)

        def ancestors_ids(self, **kwargs):
            ancestors_clauses_1, ancestors_clauses_2 = ("", "")
            query_parameters = {"id": self.id}

            limiting_fk_nodes_instance = kwargs.get("limiting_fk_nodes_instance", None)
            limiting_fk_edges_instance = kwargs.get("limiting_fk_edges_instance", None)
            excluded_nodes_queryset = kwargs.get("excluded_nodes_queryset", None)
            excluded_edges_queryset = kwargs.get("excluded_edges_queryset", None)
            required_nodes_queryset = kwargs.get("required_nodes_queryset", None)
            required_edges_queryset = kwargs.get("required_edges_queryset", None)

            if limiting_fk_nodes_instance is not None:
                pass  # Not implemented yet

            # Limits the search to nodes that connect to edges defined in a ForeignKey
            # ToDo: Currently fails in the case that the starting node is not in the
            #   set of nodes related by the ForeignKey, but is adjacend to one that is
            if limiting_fk_edges_instance is not None:
                fk_field_name = get_foreign_key_field(limiting_fk_edges_instance)
                if fk_field_name is not None:
                    ancestors_clauses_1 += "\n" + LIMITING_FK_EDGES_CLAUSE_1.format(
                        relationship_table=edge_model_table,
                        fk_field_name=fk_field_name,
                    )
                    ancestors_clauses_2 += "\n" + LIMITING_FK_EDGES_CLAUSE_2.format(
                        relationship_table=edge_model_table,
                        fk_field_name=fk_field_name,
                    )
                    query_parameters[
                        "limiting_fk_edges_instance_id"
                    ] = limiting_fk_edges_instance.id

            if excluded_nodes_queryset is not None:
                ancestors_clauses_1 += "\n" + EXCLUDED_UPWARD_NODES_CLAUSE_1.format(
                    relationship_table=edge_model_table,
                )
                ancestors_clauses_2 += "\n" + EXCLUDED_UPWARD_NODES_CLAUSE_2.format(
                    relationship_table=edge_model_table,
                )
                query_parameters["excluded_upward_node_ids"] = str(
                    set(excluded_nodes_queryset.values_list("id", flat=True))
                )

            if excluded_edges_queryset is not None:
                pass  # Not implemented yet

            if required_nodes_queryset is not None:
                pass  # Not implemented yet

            if required_edges_queryset is not None:
                pass  # Not implemented yet

            with connection.cursor() as cursor:
                cursor.execute(
                    ANCESTORS_QUERY.format(
                        relationship_table=edge_model_table,
                        ancestors_clauses_1=ancestors_clauses_1,
                        ancestors_clauses_2=ancestors_clauses_2,
                    ),
                    query_parameters,
                )
                # print(
                #     cursor.mogrify(
                #         ANCESTORS_QUERY.format(
                #             relationship_table=edge_model_table,
                #             ancestors_clauses_1=ancestors_clauses_1,
                #             ancestors_clauses_2=ancestors_clauses_2,
                #         ),
                #         query_parameters,
                #     ).decode('utf8')
                # )
                return [row[0] for row in cursor.fetchall()]

        def ancestors_and_self_ids(self, **kwargs):
            return self.ancestors_ids(**kwargs) + [self.id]

        def self_and_ancestors_ids(self, **kwargs):
            return self.ancestors_and_self_ids(**kwargs)[::-1]

        def ancestors(self, **kwargs):
            return self.filter_order_ids(self.ancestors_ids(**kwargs))

        def ancestors_and_self(self, **kwargs):
            return self.filter_order_ids(self.ancestors_and_self_ids(**kwargs))

        def self_and_ancestors(self, **kwargs):
            return self.ancestors_and_self(**kwargs)[::-1]

        def descendants_ids(self, **kwargs):
            descendants_clauses_1, descendants_clauses_2 = ("", "")
            query_parameters = {"id": self.id}

            limiting_fk_nodes_instance = kwargs.get("limiting_fk_nodes_instance", None)
            limiting_fk_edges_instance = kwargs.get("limiting_fk_edges_instance", None)
            excluded_nodes_queryset = kwargs.get("excluded_nodes_queryset", None)
            excluded_edges_queryset = kwargs.get("excluded_edges_queryset", None)
            required_nodes_queryset = kwargs.get("required_nodes_queryset", None)
            required_edges_queryset = kwargs.get("required_edges_queryset", None)

            if limiting_fk_nodes_instance is not None:
                pass  # Not implemented yet

            # Limits the search to nodes that connect to edges defined in a ForeignKey
            # ToDo: Currently fails in the case that the starting node is not in the
            #   set of nodes related by the ForeignKey, but is adjacend to one that is
            if limiting_fk_edges_instance is not None:
                fk_field_name = get_foreign_key_field(limiting_fk_edges_instance)
                if fk_field_name is not None:
                    descendants_clauses_1 += "\n" + LIMITING_FK_EDGES_CLAUSE_1.format(
                        relationship_table=edge_model_table,
                        fk_field_name=fk_field_name,
                    )
                    descendants_clauses_2 += "\n" + LIMITING_FK_EDGES_CLAUSE_2.format(
                        relationship_table=edge_model_table,
                        fk_field_name=fk_field_name,
                    )
                    query_parameters[
                        "limiting_fk_edges_instance_id"
                    ] = limiting_fk_edges_instance.id

            if excluded_nodes_queryset is not None:
                descendants_clauses_1 += "\n" + EXCLUDED_DOWNWARD_NODES_CLAUSE_1.format(
                    relationship_table=edge_model_table,
                )
                descendants_clauses_2 += "\n" + EXCLUDED_DOWNWARD_NODES_CLAUSE_2.format(
                    relationship_table=edge_model_table,
                )
                query_parameters["excluded_downward_node_ids"] = str(
                    set(excluded_nodes_queryset.values_list("id", flat=True))
                )

            if excluded_edges_queryset is not None:
                pass  # Not implemented yet

            if required_nodes_queryset is not None:
                pass  # Not implemented yet

            if required_edges_queryset is not None:
                pass  # Not implemented yet

            with connection.cursor() as cursor:
                cursor.execute(
                    DESCENDANTS_QUERY.format(
                        relationship_table=edge_model_table,
                        descendants_clauses_1=descendants_clauses_1,
                        descendants_clauses_2=descendants_clauses_2,
                    ),
                    query_parameters,
                )
                # print(
                #     cursor.mogrify(
                #         DESCENDANTS_QUERY.format(
                #             relationship_table=edge_model_table,
                #             descendants_clauses_1=descendants_clauses_1,
                #             descendants_clauses_2=descendants_clauses_2,
                #         ),
                #         query_parameters,
                #     ).decode('utf8')
                # )
                return [row[0] for row in cursor.fetchall()]

        def self_and_descendants_ids(self, **kwargs):
            return [self.id] + self.descendants_ids(**kwargs)

        def descendants_and_self_ids(self, **kwargs):
            return self.self_and_descendants_ids(**kwargs)[::-1]

        def descendants(self, **kwargs):
            return self.filter_order_ids(self.descendants_ids(**kwargs))

        def self_and_descendants(self, **kwargs):
            return self.filter_order_ids(self.self_and_descendants_ids(**kwargs))

        def descendants_and_self(self, **kwargs):
            return self.self_and_descendants(**kwargs)[::-1]

        def clan_ids(self, **kwargs):
            """
            Returns a list of ids with all ancestors, self, and all descendants
            """
            return self.ancestors_ids(**kwargs) + self.self_and_descendants_ids(
                **kwargs
            )

        def clan(self, **kwargs):
            """
            Returns a queryset with all ancestors, self, and all descendants
            """
            return self.filter_order_ids(self.clan_ids(**kwargs))

        def descendants_edges(self):
            """
            Returns a queryset of descendants edges
            """
            return edge_model.objects.filter(
                parent__id__in=self.self_and_descendants_ids(),
                child__id__in=self.self_and_descendants_ids(),
            )

        def descendants_edges_ids(self, cached_results=None):
            """
            Returns a set of descendants edges
            # ToDo: Modify to sort topologically
            """
            return list(self.descendants_edges().values_list("id", flat=True))

        def ancestors_edges(self):
            """
            Returns a queryset of ancestors edges
            """
            return edge_model.objects.filter(
                parent__id__in=self.self_and_ancestors_ids(),
                child__id__in=self.self_and_ancestors_ids(),
            )

        def ancestors_edges_ids(self, cached_results=None):
            """
            Returns a set of ancestors edges
            # ToDo: Modify to sort topologically
            """

            return list(self.ancestors_edges().values_list("id", flat=True))

        def clan_edges_ids(self):
            """
            Returns a set of all edges associated with a given node
            """
            edges = set()
            edges.update(self.descendants_edges_ids())
            edges.update(self.ancestors_edges_ids())
            return edges

        def clan_edges(self):
            """
            Returns a queryset of all edges associated with a given node
            """
            return _filter_order(edge_model.objects, "pk", self.clan_edges_ids())

        def path_ids_list(
            self, target_node, directional=True, max_depth=20, max_paths=1
        ):
            """
            Returns a list of paths from self to target node, optionally in either
            direction. The resulting lists are always sorted from root-side, toward
            leaf-side, regardless of the relative position of starting and ending nodes.

            By default, returns only one shortest path, but additional paths
            can be included by setting the max_paths argument.
            """

            # ToDo: Implement filters

            if self == target_node:
                return [[self.id]]

            
            downward_clauses, upward_clauses = ("", "")
            query_parameters = {
                "starting_node": self.id,
                "ending_node": target_node.id,
                "max_depth": max_depth,
                "max_paths": max_paths,
            }

            limiting_fk_nodes_instance = kwargs.get("limiting_fk_nodes_instance", None)
            limiting_fk_edges_instance = kwargs.get("limiting_fk_edges_instance", None)
            excluded_nodes_queryset = kwargs.get("excluded_nodes_queryset", None)
            excluded_edges_queryset = kwargs.get("excluded_edges_queryset", None)
            required_nodes_queryset = kwargs.get("required_nodes_queryset", None)
            required_edges_queryset = kwargs.get("required_edges_queryset", None)

            if limiting_fk_nodes_instance is not None:
                pass  # Not implemented yet

            if limiting_fk_edges_instance is not None:
                fk_field_name = get_foreign_key_field(limiting_fk_edges_instance)
                if fk_field_name is not None:
                    downward_clauses += "\n" + PATH_LIMITING_FK_EDGES_CLAUSE.format(
                        relationship_table=edge_model_table,
                        fk_field_name=fk_field_name,
                    )
                    query_parameters["limiting_fk_edges_instance_id"] = limiting_fk_edges_instance.id

            if excluded_nodes_queryset is not None:
                downward_clauses += "\n" + EXCLUDED_DOWNWARD_PATH_NODES_CLAUSE
                query_parameters["excluded_path_node_ids"] = str(
                    set(excluded_nodes_queryset.values_list("id", flat=True))
                )

            if excluded_edges_queryset is not None:
                pass  # Not implemented yet

            if required_nodes_queryset is not None:
                pass  # Not implemented yet

            if required_edges_queryset is not None:
                pass  # Not implemented yet
                

            with connection.cursor() as cursor:
                cursor.execute(
                    DOWNWARD_PATH_QUERY.format(
                        relationship_table=edge_model_table,
                        downward_clauses=downward_clauses
                    ),
                    query_parameters
                )
                path = [row[0] + [target_node.id] for row in cursor.fetchall()]
                if not path and not directional:

                    if limiting_fk_nodes_instance is not None:
                        pass  # Not implemented yet

                    if limiting_fk_edges_instance is not None:
                        pass  # Not implemented yet


                    if limiting_fk_edges_instance is not None:
                        if 'fk_field_name' in locals():
                            upward_clauses += "\n" + PATH_LIMITING_FK_EDGES_CLAUSE.format(
                                relationship_table=edge_model_table,
                                fk_field_name=fk_field_name,
                            )

                    if excluded_nodes_queryset is not None:
                        upward_clauses += "\n" + EXCLUDED_UPWARD_PATH_NODES_CLAUSE
                        query_parameters["excluded_path_node_ids"] = str(
                            set(excluded_nodes_queryset.values_list("id", flat=True))
                        )

                    if excluded_edges_queryset is not None:
                        pass  # Not implemented yet

                    if required_nodes_queryset is not None:
                        pass  # Not implemented yet

                    if required_edges_queryset is not None:
                        pass  # Not implemented yet

                    with connection.cursor() as cursor:
                        cursor.execute(
                            UPWARD_PATH_QUERY.format(
                                relationship_table=edge_model_table,
                                upward_clauses=upward_clauses
                            ),
                            query_parameters
                        )
                        path = [
                            [target_node.id] + row[0][::-1] for row in cursor.fetchall()
                        ]
                if not path:
                    raise NodeNotReachableException
                return path

        def shortest_path(self, target_node, directional=True, max_depth=20):
            """
            Returns a queryset of the shortest path
            """
            return self.filter_order_ids(
                self.path_ids_list(
                    target_node, directional=directional, max_depth=max_depth
                )[0]
            )

        def distance(self, target_node, directional=True, max_depth=20):
            """
            Returns the shortest hops count to the target node
            """
            return (
                len(
                    self.path_ids_list(
                        target_node, directional=directional, max_depth=max_depth
                    )[0]
                )
                - 1
            )

        def is_root(self):
            """
            Check if has children and not ancestors
            """
            return bool(self.children.exists() and not self.parents.exists())

        def is_leaf(self):
            """
            Check if has ancestors and not children
            """
            return bool(self.parents.exists() and not self.children.exists())

        def is_island(self):
            """
            Check if has no ancestors nor children
            """
            return bool(not self.children.exists() and not self.parents.exists())

        def descendants_tree(self):
            """
            Returns a tree-like structure with descendants
            # ToDo: Modify to use CTE
            """
            tree = {}
            for child in self.children.all():
                tree[child] = child.descendants_tree()
            return tree

        def ancestors_tree(self):
            """
            Returns a tree-like structure with ancestors
            # ToDo: Modify to use CTE
            """
            tree = {}
            for parent in self.parents.all():
                tree[parent] = parent.ancestors_tree()
            return tree

        def _get_roots(self, ancestors_tree):
            """
            Works on objects: no queries
            """
            if not ancestors_tree:
                return set([self])
            roots = set()
            for ancestor in ancestors_tree:
                roots.update(ancestor._get_roots(ancestors_tree[ancestor]))
            return roots

        def get_roots(self):
            """
            Returns roots nodes, if any
            # ToDo: Modify to use CTE
            """
            ancestors_tree = self.ancestors_tree()
            roots = set()
            for ancestor in ancestors_tree:
                roots.update(ancestor._get_roots(ancestors_tree[ancestor]))
            return roots

        def _get_leaves(self, descendants_tree):
            """
            Works on objects: no queries
            """
            if not descendants_tree:
                return set([self])
            leaves = set()
            for descendant in descendants_tree:
                leaves.update(descendant._get_leaves(descendants_tree[descendant]))
            return leaves

        def get_leaves(self):
            """
            Returns leaves nodes, if any
            # ToDo: Modify to use CTE
            """
            descendants_tree = self.descendants_tree()
            leaves = set()
            for descendant in descendants_tree:
                leaves.update(descendant._get_leaves(descendants_tree[descendant]))
            return leaves

        @staticmethod
        def circular_checker(parent, child):
            if child.id in parent.self_and_ancestors_ids():
                raise ValidationError("The object is an ancestor.")

    return Node


class EdgeManager(models.Manager):
    def descendants(self, node):
        """
        Returns a queryset of all edges descended from the given node
        """
        return _filter_order(
            self.model.objects, "parent_id", node.self_and_descendants_ids()
        )

    def ancestors(self, node):
        """
        Returns a queryset of all edges which are ancestors of the given node
        """
        return _filter_order(
            self.model.objects, "child_id", node.self_and_ancestors_ids()
        )

    def clan(self, node):
        """
        Returns a queryset of all edges for ancestors, self, and descendants
        """
        return _filter_order(
            self.model.objects, ["parent_id", "child_id"], node.clan_ids()
        )

    def shortest_path(self, start_node, end_node):
        """
        Returns a queryset of all edges for the shortest path from start_node to end_node
        """
        return _filter_order(
            self.model.objects,
            ["parent_id", "child_id"],
            start_node.path_ids_list(end_node)[0],
        )

    def validate_route(self, edges):
        """
        Given a list or set of edges, verify that they result in a contiguous route
        """
        # ToDo: Implement
        pass

    def sort(self, edges):
        """
        Given a list or set of edges, sort them from root-side to leaf-side
        """
        # ToDo: Implement
        pass


def edge_factory(
    node_model,
    child_to_field="id",
    parent_to_field="id",
    concrete=True,
    base_model=models.Model,
):
    if isinstance(node_model, str):
        try:
            node_model_name = node_model.split(".")[1]
        except IndexError:
            node_model_name = node_model
    else:
        node_model_name = node_model._meta.model_name

    class Edge(base_model):
        parent = models.ForeignKey(
            node_model,
            related_name=f"{node_model_name}_child",
            to_field=parent_to_field,
            on_delete=models.CASCADE,
        )
        child = models.ForeignKey(
            node_model,
            related_name=f"{node_model_name}_parent",
            to_field=child_to_field,
            on_delete=models.CASCADE,
        )

        objects = EdgeManager()

        class Meta:
            abstract = not concrete

        def save(self, *args, **kwargs):
            if not kwargs.pop("disable_circular_check", False):
                self.parent.__class__.circular_checker(self.parent, self.child)
            super(Edge, self).save(*args, **kwargs)

    return Edge
