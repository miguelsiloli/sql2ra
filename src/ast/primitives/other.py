from .ast_base import ASTNode


class FunctionName(ASTNode):
    """
    Represents the name of a function in an SQL query.

    The FunctionName class is used to represent the name of a function (e.g., COUNT, SUM)
    in the abstract syntax tree (AST) of an SQL query.

    :param name: The name of the function.
    """

    def __init__(self, name: str):
        """
        Initializes the FunctionName instance with the given function name.

        :param name: The name of the function.
        """
        super().__init__("FunctionName", [name])
        self.name = name

    def to_dict(self) -> dict:
        """
        Converts the FunctionName instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "FunctionName", "name": "function_name"}.
        """
        return {"node_type": self.node_type, "name": self.name}


class Literal(ASTNode):
    """
    Represents a literal value in an SQL query.

    The Literal class is used to represent a literal value (e.g., a string, number)
    in the abstract syntax tree (AST) of an SQL query.

    :param value: The literal value as a string.
    """

    def __init__(self, value: str):
        """
        Initializes the Literal instance with the given value.

        :param value: The literal value as a string.
        """
        super().__init__("Literal", [value])

    def to_dict(self) -> dict:
        """
        Converts the Literal instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "Literal", "value": "literal_value"}.
        """
        return {"node_type": self.node_type, "value": self.children[0]}


class GroupByItem(ASTNode):
    """
    Represents an item in the GROUP BY clause of an SQL query.

    The GroupByItem class is used to represent an expression (e.g., a column or function)
    that appears in the GROUP BY clause of an SQL query.

    :param expression: An ASTNode representing the expression in the GROUP BY clause.
    """

    def __init__(self, expression: ASTNode):
        """
        Initializes the GroupByItem instance with the given expression.

        :param expression: An ASTNode representing the expression in the GROUP BY clause.
        """
        super().__init__("GroupByItem", [expression])


class Subquery(ASTNode):
    """
    Represents a subquery in an SQL query.

    The Subquery class is used to represent a subquery within an SQL statement,
    such as in the FROM clause or as part of a WHERE clause.

    :param query: An ASTNode representing the subquery.
    """

    def __init__(self, query: ASTNode):
        """
        Initializes the Subquery instance with the given query.

        :param query: An ASTNode representing the subquery.
        """
        super().__init__("Subquery", [query])
        self.query = query

    def to_dict(self) -> dict:
        """
        Converts the Subquery instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "Subquery", "children": [subquery_dict]}.
        """
        return {
            "node_type": self.node_type,
            "children": [self.query.to_dict()],  # Convert the query node to dict
        }
