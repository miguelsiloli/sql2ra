from typing import Optional
from ..primitives import ASTNode, Literal
from ..derived_types import HavingClause, Comparison, Identifier, LogicalOperation, FunctionCall


class HavingClauseParser:
    """
    A parser for the HAVING clause in an SQL statement.

    The HavingClauseParser class is responsible for parsing the HAVING clause,
    including conditions, comparisons, and logical operations within the clause.
    """

    def __init__(self, parser):
        """
        Initializes the HavingClauseParser with a Parser instance.

        :param parser: An instance of the Parser class used for token consumption and lookahead.
        """
        self.parser = parser

    def parse_having(self) -> Optional[HavingClause]:
        """
        Parses the HAVING clause of an SQL statement if it exists.

        This method checks if the current token represents a HAVING clause.
        If a HAVING clause is found, it parses the condition(s) inside the
        clause and returns a HavingClause object. If no HAVING clause is
        found, it returns None.

        :return: A HavingClause object representing the parsed HAVING clause, or None if the clause is not present.
        """
        # Check if the current token is 'HAVING'
        if not (
            self.parser.current_token()
            and self.parser.current_token().type == "KEYWORD"
            and self.parser.current_token().value.upper() == "HAVING"
        ):
            return None  # No HAVING clause present

        # Consume the 'HAVING' token
        self.parser.consume("KEYWORD", "HAVING")

        # Parse the condition inside the HAVING clause
        condition = self.parse_condition()

        if condition:
            return HavingClause(condition)
        else:
            return None

    def parse_condition(self) -> ASTNode:
        """
        Parses a condition inside the HAVING clause, including comparisons and logical operations.

        This method parses conditions within the HAVING clause, including
        comparisons (e.g., column1 > 100) and logical operations (e.g.,
        AND, OR). It constructs an abstract syntax tree (AST) representing
        the condition.

        :return: An ASTNode representing the parsed condition.
        """
        # Start by parsing the left-hand side of the comparison, which could be an identifier or a function
        left = self.parse_expression()

        # Check if there is a comparison operator
        if self.parser.current_token() and self.parser.current_token().type == "OPERATOR":
            operator = self.parser.consume("OPERATOR").value

            # Parse the right-hand side of the comparison, which could be a literal or an expression
            right = self.parse_expression()

            # Return a Comparison node
            return Comparison(left, operator, right)

        # If the current token is a logical operator, we need to parse a logical operation
        while (
            self.parser.current_token()
            and self.parser.current_token().type == "KEYWORD"
            and self.parser.current_token().value.upper() in ["AND", "OR"]
        ):
            operator = self.parser.consume("KEYWORD").value.upper()

            # Recursively parse the right-hand side condition
            right = self.parse_condition()

            # Combine the left and right sides into a LogicalOperation node
            left = LogicalOperation(left, operator, right)

        return left

    def parse_identifier(self) -> Identifier:
        """
        Parses an identifier, such as a column name.

        This method consumes an identifier token and returns an Identifier object.

        :return: An Identifier object.
        """
        return Identifier(self.parser.consume("IDENTIFIER").value)

    def parse_expression(self) -> ASTNode:
        """
        Parses an expression, which could be an identifier, a function, or a literal.

        :return: An ASTNode representing the parsed expression.
        """
        current_token = self.parser.current_token()

        if current_token.type == "IDENTIFIER":
            return self.parse_identifier()

        elif current_token.type == "KEYWORD" and current_token.value.upper() in [
            "COUNT",
            "SUM",
            "AVG",
            "MIN",
            "MAX",
        ]:
            return self.parse_function()

        elif current_token.type in ["NUMBER", "STRING"]:
            return Literal(self.parser.consume(current_token.type).value)

        else:
            raise Exception(f"Unexpected token in expression: {current_token}")

    # def parse_identifier(self) -> Identifier:
    #     """
    #     Parses an identifier, such as a column name.

    #     :return: An Identifier object.
    #     """
    #     return Identifier(self.parser.consume('IDENTIFIER').value)

    def parse_function(self) -> FunctionCall:
        """
        Parses a function call, such as COUNT, SUM, etc.

        :return: A FunctionCall object representing the parsed function call.
        """
        function_name = self.parser.consume(
            "KEYWORD"
        ).value  # or 'KEYWORD' if functions are classified as keywords

        # Consume '('
        self.parser.consume("PUNCTUATION", "(")

        # Parse the argument(s) inside the function
        arguments = []

        # Handle special case like COUNT(*)
        if (
            self.parser.current_token().type == "WILDCARD"
            and self.parser.current_token().value == "*"
        ):
            arguments.append(Literal(self.parser.consume("WILDCARD").value))
        else:
            while (
                self.parser.current_token().type != "PUNCTUATION"
                or self.parser.current_token().value != ")"
            ):
                arguments.append(self.parse_expression())
                if (
                    self.parser.current_token().type == "PUNCTUATION"
                    and self.parser.current_token().value == ","
                ):
                    self.parser.consume("PUNCTUATION", ",")

        # Consume ')'
        self.parser.consume("PUNCTUATION", ")")

        return FunctionCall(function_name, arguments)
