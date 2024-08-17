from ..primitives.ast_base import ASTNode
from typing import Optional, List, Dict
from .components import SelectItem


class SelectClause(ASTNode):
    """
    Represents the SELECT clause in an SQL query.

    The SelectClause class is used to represent the list of items selected in the
    SELECT clause of an SQL query.

    :param children: A list of SelectItem objects representing the selected items.
    """

    def __init__(self, children: List[SelectItem]):
        """
        Initializes the SelectClause instance with the given list of selected items.

        :param children: A list of SelectItem objects representing the selected items.
        """
        self.node_type = "SelectClause"
        self.children = children

    def __repr__(self):
        """
        Returns a string representation of the SelectClause instance.

        :return: A string in the format "SelectClause(children=[...])".
        """
        return f"SelectClause(children={self.children})"

    def to_dict(self) -> Dict:
        """
        Converts the SelectClause instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "SelectClause", "children": [...]}.
        """
        return {
            "node_type": self.node_type,
            "children": [child.to_dict() for child in self.children],
        }


class FromClause(ASTNode):
    """
    Represents the FROM clause in an SQL query.

    The FromClause class is used to represent the table or subquery from which data is selected
    in the abstract syntax tree (AST) of an SQL query.

    :param table: The table or subquery being selected from.
    """

    def __init__(self, table):
        """
        Initializes the FromClause instance with the given table or subquery.

        :param table: The table or subquery being selected from.
        """
        super().__init__("FromClause", [table])
        self.table = table

    def to_dict(self) -> dict:
        """
        Converts the FromClause instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "FromClause", "table": {...}}.
        """
        return {"node_type": self.node_type, "table": self.table[0].to_dict()}


class OrderByClause(ASTNode):
    """
    Represents the ORDER BY clause in an SQL query.

    The OrderByClause class is used to represent the list of items used to order the result set
    in the abstract syntax tree (AST) of an SQL query.

    :param children: An optional list of ASTNode objects representing the ordering items.
    """

    def __init__(self, children: Optional[List[ASTNode]] = None):
        """
        Initializes the OrderByClause instance with the given list of ordering items.

        :param children: An optional list of ASTNode objects representing the ordering items.
        """
        super().__init__("OrderByClause", children)

    def to_dict(self) -> dict:
        """
        Converts the OrderByClause instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "OrderByClause", "children": [...]}.
        """
        return {
            "node_type": self.node_type,
            "children": [child.to_dict() for child in self.children] if self.children else [],
        }


class WhereClause(ASTNode):
    """
    Represents the WHERE clause in an SQL query.

    The WhereClause class is used to represent the conditions applied to filter the result set
    in the abstract syntax tree (AST) of an SQL query.

    :param condition: A list of ASTNode objects representing the conditions in the WHERE clause.
    """

    def __init__(self, condition: List[ASTNode]):
        """
        Initializes the WhereClause instance with the given list of conditions.

        :param condition: A list of ASTNode objects representing the conditions in the WHERE clause.
        """
        super().__init__("WhereClause", condition)
        self.condition = condition

    def to_dict(self) -> dict:
        """
        Converts the WhereClause instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "WhereClause", "conditions": [...]}.
        """
        conditions_dict = [cond.to_dict() for cond in self.condition]

        return {"node_type": self.node_type, "conditions": conditions_dict}


class GroupByClause(ASTNode):
    """
    Represents the GROUP BY clause in an SQL query.

    The GroupByClause class is used to represent the list of columns or expressions
    used to group the result set in the abstract syntax tree (AST) of an SQL query.

    :param children: An optional list of ASTNode objects representing the grouping items.
    """

    def __init__(self, children: Optional[List[ASTNode]] = None):
        """
        Initializes the GroupByClause instance with the given list of grouping items.

        :param children: An optional list of ASTNode objects representing the grouping items.
        """
        super().__init__("GroupByClause", children)

    def to_dict(self) -> Dict:
        """
        Converts the GroupByClause instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "GroupByClause", "children": [...]}.
        """
        return {
            "node_type": self.node_type,
            "children": [child.to_dict() for child in self.children],
        }


class JoinClause(ASTNode):
    """
    Represents a JOIN clause in an SQL query.

    The JoinClause class is used to represent a JOIN operation between tables
    in the abstract syntax tree (AST) of an SQL query.

    :param join_type: The type of JOIN (e.g., INNER JOIN, LEFT JOIN).
    :param table: The table being joined.
    :param condition: The condition on which the join is based.
    """

    def __init__(self, join_type: str, table: ASTNode, condition: ASTNode):
        """
        Initializes the JoinClause instance with the join type, table, and condition.

        :param join_type: The type of JOIN (e.g., INNER JOIN, LEFT JOIN).
        :param table: The table being joined.
        :param condition: The condition on which the join is based.
        """
        super().__init__("JoinClause", [table, condition])
        self.join_type = join_type
        self.table = table
        self.condition = condition

    def to_dict(self) -> dict:
        """
        Converts the JoinClause instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "JoinClause", "join_type": ..., "table": ..., "condition": ...}.
        """
        return {
            "node_type": self.node_type,
            "join_type": self.join_type,
            "table": self.table.to_dict(),
            "condition": self.condition.to_dict(),
        }


class HavingClause(ASTNode):
    """
    Represents the HAVING clause in an SQL query.

    The HavingClause class is used to represent the conditions applied to filter the result set
    after grouping in the abstract syntax tree (AST) of an SQL query.

    :param condition: The condition applied in the HAVING clause.
    """

    def __init__(self, condition):
        """
        Initializes the HavingClause instance with the given condition.

        :param condition: The condition applied in the HAVING clause.
        """
        super().__init__("HavingClause", [condition])
        self.condition = condition

    def to_dict(self):
        """
        Converts the HavingClause instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "HavingClause", "condition": {...}}.
        """
        return {"node_type": self.node_type, "condition": self.condition.to_dict()}
