from ..primitives.ast_base import ASTNode
from typing import Optional, List, Dict


class SelectItem(ASTNode):
    """
    Represents an item in the SELECT clause of an SQL query.

    The SelectItem class is used to represent an expression in the SELECT clause,
    optionally with an alias.

    :param expression: The expression being selected.
    :param alias: An optional alias for the selected expression.
    """

    def __init__(self, expression: ASTNode, alias: Optional[str] = None):
        """
        Initializes the SelectItem instance with the expression and optional alias.

        :param expression: The expression being selected.
        :param alias: An optional alias for the selected expression.
        """
        super().__init__("SelectItem", [expression])
        self.expression = expression
        self.alias = alias

    def to_dict(self) -> dict:
        """
        Converts the SelectItem instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "SelectItem", "expression": ..., "alias": ...}.
        """
        result = super().to_dict()
        result["expression"] = self.expression.to_dict()
        if self.alias:
            result["alias"] = self.alias
        return result


class Identifier(ASTNode):
    """
    Represents an identifier in an SQL query.

    The Identifier class is used to represent a named element, such as a column or table name,
    in the abstract syntax tree (AST) of an SQL query.

    :param name: The name of the identifier.
    """

    def __init__(self, name: str):
        """
        Initializes the Identifier instance with the given name.

        :param name: The name of the identifier.
        """
        super().__init__("Identifier")
        self.name = name

    def to_dict(self) -> dict:
        """
        Converts the Identifier instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "Identifier", "name": "identifier_name"}.
        """
        result = super().to_dict()
        result["name"] = self.name
        return result


class Order(ASTNode):
    """
    Represents an ORDER BY item in an SQL query.

    The Order class is used to represent an ordering clause for a specific column,
    optionally with an order direction (ASC or DESC).

    :param column: The column to be ordered.
    :param order: The optional order direction (ASC or DESC).
    """

    def __init__(self, column: Identifier, order: Optional[str] = None):
        """
        Initializes the Order instance with the column and optional order direction.

        :param column: The column to be ordered.
        :param order: The optional order direction (ASC or DESC).
        """
        super().__init__("Order", [column])
        self.column = column
        self.order = order

    def to_dict(self) -> dict:
        """
        Converts the Order instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "Order", "column": ..., "order": ...}.
        """
        result = {"node_type": self.node_type, "column": self.column.to_dict()}
        if self.order:
            result["order"] = self.order
        return result


class FunctionCall(ASTNode):
    """
    Represents a function call in an SQL query.

    The FunctionCall class is used to represent a function call (e.g., COUNT, SUM) with arguments
    in the abstract syntax tree (AST) of an SQL query.

    :param name: The name of the function being called.
    :param arguments: A list of arguments passed to the function.
    """

    def __init__(self, name: str, arguments: List[ASTNode]):
        """
        Initializes the FunctionCall instance with the function name and arguments.

        :param name: The name of the function being called.
        :param arguments: A list of arguments passed to the function.
        """
        super().__init__("FunctionCall", arguments)
        self.name = name
        self.arguments = arguments

    def to_dict(self) -> Dict:
        """
        Converts the FunctionCall instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "FunctionCall", "name": "function_name", "arguments": [...]}.
        """
        return {
            "node_type": self.node_type,
            "name": self.name,
            "arguments": [arg.to_dict() for arg in self.arguments],
        }


class TableReference(ASTNode):
    """
    Represents a table reference in the FROM clause of an SQL query.

    The TableReference class is used to represent a table name, optionally with an alias,
    in the abstract syntax tree (AST) of an SQL query.

    :param table_name: The name of the table being referenced.
    :param alias: An optional alias for the table.
    """

    def __init__(self, table_name: str, alias: Optional[str] = None):
        """
        Initializes the TableReference instance with the table name and optional alias.

        :param table_name: The name of the table being referenced.
        :param alias: An optional alias for the table.
        """
        super().__init__("TableReference", [table_name, alias] if alias else [table_name])

    def to_dict(self) -> dict:
        """
        Converts the TableReference instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "TableReference", "table_name": ..., "alias": ...}.
        """
        return {
            "node_type": self.node_type,
            "table_name": self.children[0],
            "alias": self.children[1] if len(self.children) > 1 else None,
        }


class Wildcard(ASTNode):
    """
    Represents a wildcard (*) in an SQL query.

    The Wildcard class is used to represent the * symbol in the SELECT clause
    of an SQL query, which selects all columns.

    """

    def __init__(self):
        """
        Initializes the Wildcard instance.
        """
        super().__init__("Wildcard", ["*"])

    def to_dict(self) -> dict:
        """
        Converts the Wildcard instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "Wildcard", "value": "*"}.
        """
        return {"node_type": self.node_type, "value": self.children[0]}


class GroupBy(ASTNode):
    """
    Represents the GROUP BY clause in an SQL query.

    The GroupBy class is used to represent a list of columns or expressions
    in the GROUP BY clause of an SQL query.

    :param columns: A list of columns or expressions to group by.
    """

    def __init__(self, columns: List[ASTNode]):
        """
        Initializes the GroupBy instance with a list of columns or expressions.

        :param columns: A list of columns or expressions to group by.
        """
        self.node_type = "GroupBy"
        self.columns = columns

    def __repr__(self):
        """
        Returns a string representation of the GroupBy instance.

        :return: A string in the format "GroupBy(columns=[...])".
        """
        return f"GroupBy(columns={self.columns})"

    def to_dict(self) -> dict:
        """
        Converts the GroupBy instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "GroupBy", "columns": [...]}.
        """
        return {
            "node_type": self.node_type,
            "columns": [column.to_dict() for column in self.columns],
        }
