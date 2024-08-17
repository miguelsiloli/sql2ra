from ..primitives.ast_base import ASTNode
from typing import List


class LogicalOperation(ASTNode):
    """
    Represents a logical operation (e.g., AND, OR) in an SQL query.

    The LogicalOperation class is used to represent a logical operation between two
    expressions in the abstract syntax tree (AST) of an SQL query.

    :param left: The left-hand side of the logical operation.
    :param operator: The logical operator (e.g., AND, OR).
    :param right: The right-hand side of the logical operation.
    """

    def __init__(self, left: ASTNode, operator: str, right: ASTNode):
        """
        Initializes the LogicalOperation instance with the left and right operands and the operator.

        :param left: The left-hand side of the logical operation.
        :param operator: The logical operator (e.g., AND, OR).
        :param right: The right-hand side of the logical operation.
        """
        super().__init__("LogicalOperation", [left, right])
        self.operator = operator

    def to_dict(self) -> dict:
        """
        Converts the LogicalOperation instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "LogicalOperation", "left": ..., "operator": ..., "right": ...}.
        """
        return {
            "node_type": self.node_type,
            "left": self.children[0].to_dict(),
            "operator": self.operator,
            "right": self.children[1].to_dict(),
        }


class Like(ASTNode):
    """
    Represents a LIKE operation in an SQL query.

    The Like class is used to represent a LIKE pattern matching operation between
    an expression and a pattern in the abstract syntax tree (AST) of an SQL query.

    :param left: The expression to be matched.
    :param pattern: The pattern to match against.
    """

    def __init__(self, left: ASTNode, pattern: ASTNode):
        """
        Initializes the Like instance with the expression and pattern.

        :param left: The expression to be matched.
        :param pattern: The pattern to match against.
        """
        super().__init__("Like", [left, pattern])

    def to_dict(self) -> dict:
        """
        Converts the Like instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "Like", "left": ..., "pattern": ...}.
        """
        return {
            "node_type": self.node_type,
            "left": self.children[0].to_dict(),
            "pattern": self.children[1].to_dict(),
        }


class UnaryOperation(ASTNode):
    """
    Represents a unary operation (e.g., NOT) in an SQL query.

    The UnaryOperation class is used to represent a unary operation applied to a single
    operand in the abstract syntax tree (AST) of an SQL query.

    :param operator: The unary operator (e.g., NOT).
    :param operand: The operand on which the unary operation is applied.
    """

    def __init__(self, operator: str, operand: ASTNode):
        """
        Initializes the UnaryOperation instance with the operator and operand.

        :param operator: The unary operator (e.g., NOT).
        :param operand: The operand on which the unary operation is applied.
        """
        super().__init__("UnaryOperation", [operand])
        self.operator = operator

    def to_dict(self) -> dict:
        """
        Converts the UnaryOperation instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "UnaryOperation", "operator": ..., "operand": ...}.
        """
        return {
            "node_type": self.node_type,
            "operator": self.operator,
            "operand": self.children[0].to_dict(),
        }


class Comparison(ASTNode):
    """
    Represents a comparison operation (e.g., =, >, <) in an SQL query.

    The Comparison class is used to represent a comparison between two expressions
    in the abstract syntax tree (AST) of an SQL query.

    :param left: The left-hand side of the comparison.
    :param operator: The comparison operator.
    :param right: The right-hand side of the comparison.
    """

    def __init__(self, left: ASTNode, operator: ASTNode, right: ASTNode):
        """
        Initializes the Comparison instance with the left and right operands and the operator.

        :param left: The left-hand side of the comparison.
        :param operator: The comparison operator.
        :param right: The right-hand side of the comparison.
        """
        super().__init__("Comparison", [left, operator, right])

    def to_dict(self) -> dict:
        """
        Converts the Comparison instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "Comparison", "left": ..., "operator": ..., "right": ...}.
        """
        return {
            "node_type": self.node_type,
            "left": self.children[0].to_dict(),
            "operator": self.children[1],
            "right": self.children[2].to_dict(),
        }


class InList(ASTNode):
    """
    Represents an IN list operation in an SQL query.

    The InList class is used to represent an expression that is checked against
    a list of values in the abstract syntax tree (AST) of an SQL query.

    :param expression: The expression being checked.
    :param values: A list of values against which the expression is checked.
    """

    def __init__(self, expression: ASTNode, values: List[ASTNode]):
        """
        Initializes the InList instance with the expression and list of values.

        :param expression: The expression being checked.
        :param values: A list of values against which the expression is checked.
        """
        super().__init__("InList", [expression] + values)
        self.expression = expression
        self.values = values

    def to_dict(self) -> dict:
        """
        Converts the InList instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "InList", "expression": ..., "values": [...]}.
        """
        return {
            "node_type": self.node_type,
            "expression": self.expression.to_dict(),
            "values": [value.to_dict() for value in self.values],
        }


class Between(ASTNode):
    """
    Represents a BETWEEN operation in an SQL query.

    The Between class is used to represent a BETWEEN operation that checks whether
    an expression falls within a specified range in the abstract syntax tree (AST) of an SQL query.

    :param expression: The expression being checked.
    :param lower: The lower bound of the range.
    :param upper: The upper bound of the range.
    """

    def __init__(self, expression: ASTNode, lower: ASTNode, upper: ASTNode):
        """
        Initializes the Between instance with the expression, lower bound, and upper bound.

        :param expression: The expression being checked.
        :param lower: The lower bound of the range.
        :param upper: The upper bound of the range.
        """
        super().__init__("Between", [expression, lower, upper])
        self.expression = expression
        self.lower = lower
        self.upper = upper

    def to_dict(self) -> dict:
        """
        Converts the Between instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "Between", "expression": ..., "lower": ..., "upper": ...}.
        """
        return {
            "node_type": self.node_type,
            "expression": self.expression.to_dict(),
            "lower": self.lower.to_dict(),
            "upper": self.upper.to_dict(),
        }


class IsNullOperation(ASTNode):
    """
    Represents an IS NULL or IS NOT NULL operation in an SQL query.

    The IsNullOperation class is used to represent a check for null values in an expression,
    optionally with negation (IS NOT NULL), in the abstract syntax tree (AST) of an SQL query.

    :param expression: The expression being checked for null values.
    :param negation: A boolean indicating whether the operation is negated (IS NOT NULL).
    """

    def __init__(self, expression: ASTNode, negation: bool = False):
        """
        Initializes the IsNullOperation instance with the expression and negation flag.

        :param expression: The expression being checked for null values.
        :param negation: A boolean indicating whether the operation is negated (IS NOT NULL).
        """
        self.node_type = "IsNullOperation"
        self.expression = expression
        self.negation = negation
        self.children = [expression]

    def __repr__(self):
        """
        Returns a string representation of the IsNullOperation instance.

        :return: A string in the format "IsNullOperation(expression=..., negation=...)".
        """
        return f"IsNullOperation(expression={self.expression}, negation={self.negation})"

    def to_dict(self) -> dict:
        """
        Converts the IsNullOperation instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "IsNullOperation", "negation": ..., "children": [...]}.
        """
        return {
            "node_type": self.node_type,
            "negation": self.negation,
            "children": [child.to_dict() for child in self.children],
        }
