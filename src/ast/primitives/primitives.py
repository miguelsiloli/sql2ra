from .ast_base import ASTNode


class Operator(ASTNode):
    """
    Represents an operator in an SQL query.

    The Operator class is used to represent an operator (e.g., '=', '>', '<') in the
    abstract syntax tree (AST) of an SQL query.

    :param operator: The operator as a string.
    """

    def __init__(self, operator: str):
        """
        Initializes the Operator instance with the given operator.

        :param operator: The operator as a string.
        """
        super().__init__("Operator", [operator])

    def to_dict(self) -> dict:
        """
        Converts the Operator instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "Operator", "operator": "operator"}.
        """
        return {"node_type": self.node_type, "operator": self.children[0]}


class BooleanLiteral(ASTNode):
    """
    Represents a boolean literal in an SQL query.

    The BooleanLiteral class is used to represent boolean values (TRUE or FALSE)
    in the abstract syntax tree (AST) of an SQL query.

    :param value: The boolean value as a string ("TRUE" or "FALSE").
    """

    def __init__(self, value: str):
        """
        Initializes the BooleanLiteral instance with the given boolean value.

        :param value: The boolean value as a string ("TRUE" or "FALSE").
        """
        self.node_type = "Boolean"
        self.value = value.upper()  # Ensure that the value is standardized as 'TRUE' or 'FALSE'

    def __repr__(self):
        """
        Returns a string representation of the BooleanLiteral instance.

        :return: A string in the format "BooleanLiteral(value=TRUE)" or "BooleanLiteral(value=FALSE)".
        """
        return f"BooleanLiteral(value={self.value})"


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
