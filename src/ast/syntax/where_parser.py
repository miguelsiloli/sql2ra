from ..primitives import (
    ASTNode,
    Optional,
    Literal,
    Subquery,
    Operator,
    BooleanLiteral,
)
from ..derived_types import (
    WhereClause,
    LogicalOperation,
    Identifier,
    InList,
    IsNullOperation,
    Between,
    Comparison,
    UnaryOperation,
)
from typing import List


class WhereParser:
    def __init__(self, parser):
        """
        Initializes a WhereParser instance with a parser object.

        Args:
            parser: The parser object to be used by the WhereParser instance.

        Returns:
            None
        """
        self.parser = parser

    def find_where_clause(self) -> bool:
        """
        Scans through the tokens to find the WHERE clause.
        If found, it consumes the WHERE keyword and returns True.
        If not found, it returns False.
        """
        while self.parser.current_token():
            current_token = self.parser.current_token()
            if current_token.type == "KEYWORD" and current_token.value.upper() == "WHERE":
                self.parser.consume("KEYWORD", "WHERE")
                return True
            self.parser.consume(current_token.type)  # Consume non-WHERE tokens
        return False

    def parse_where(self) -> Optional[WhereClause]:
        """
        Parses the WHERE clause of a SQL query.

        This function searches for the WHERE clause in the SQL query and parses it to extract the conditions.
        It uses a stack-based approach to handle the precedence of operators and the grouping of conditions.

        Returns:
            Optional[WhereClause]: If the WHERE clause is found, it returns a `WhereClause` object containing the parsed conditions.
                                 If the WHERE clause is not found, it returns `None`.
        """
        if not self.find_where_clause():
            return None  # No WHERE clause found

        # conditions = []
        operator_stack = []
        condition_stack = []

        while True:
            try:
                current_token = self.parser.current_token()

                if not current_token:
                    break

                if current_token.type == "PUNCTUATION" and current_token.value == "(":
                    operator_stack.append("(")
                    self.parser.consume("PUNCTUATION", "(")
                elif current_token.type == "PUNCTUATION" and current_token.value == ")":
                    while operator_stack and operator_stack[-1] != "(":
                        right = condition_stack.pop()
                        left = condition_stack.pop()
                        op = operator_stack.pop()
                        condition_stack.append(LogicalOperation(left, op, right))
                    if operator_stack and operator_stack[-1] == "(":
                        operator_stack.pop()
                    self.parser.consume("PUNCTUATION", ")")
                elif current_token.type == "KEYWORD" and current_token.value.upper() in [
                    "AND",
                    "OR",
                ]:
                    while operator_stack and operator_stack[-1] in ["AND", "OR"]:
                        right = condition_stack.pop()
                        left = condition_stack.pop()
                        op = operator_stack.pop()
                        condition_stack.append(LogicalOperation(left, op, right))
                    operator_stack.append(current_token.value.upper())
                    self.parser.consume("KEYWORD", current_token.value)
                else:
                    condition = self.parse_condition()
                    if condition:
                        condition_stack.append(condition)
                    else:
                        break

            except Exception as e:
                # Handle unexpected clauses or unparseable items like 'ORDER BY', 'GROUP BY', etc.
                print(f"Parsing error encountered: {e}")
                break  # Exit the loop and return the current results

        # Combine the conditions into the final WhereClause
        while operator_stack:
            right = condition_stack.pop()
            left = condition_stack.pop()
            op = operator_stack.pop()
            condition_stack.append(LogicalOperation(left, op, right))

        if condition_stack:
            return WhereClause([condition_stack[0]])
        else:
            return None

    def parse_comparison(self) -> ASTNode:
        """
        Parses a comparison operation from the current token stream.

        Returns an ASTNode representing the parsed comparison operation.
        If no operator is present, returns the result of parse_expression.
        """
        left = self.parse_expression()
        if self.parser.current_token() and self.parser.current_token().type == "OPERATOR":
            operator = self.parser.consume("OPERATOR").value
            right = self.parse_expression()
            return Comparison(left, operator, right)
        return left

    def parse_expression(self) -> ASTNode:
        """
        Parses an expression in the WHERE clause.

        :return: An ASTNode representing the parsed expression.
        """
        current_token = self.parser.current_token()

        # Ignore `ORDER BY` and other irrelevant clauses
        if current_token.type == "KEYWORD" and current_token.value.upper() in [
            "ORDER BY",
            "GROUP BY",
            "LIMIT",
        ]:
            raise Exception(f"Irrelevant token in expression: {current_token}")

        if current_token.type == "IDENTIFIER":
            return self.parse_identifier()
        elif current_token.type == "LITERAL":
            return Literal(self.parser.consume("LITERAL").value)
        elif current_token.type == "NUMBER":
            return Literal(self.parser.consume("NUMBER").value)  # Handle numeric literals
        elif current_token.type == "STRING":
            return Literal(self.parser.consume("STRING").value)  # Handle string literals
        elif current_token.type == "PUNCTUATION" and current_token.value == "(":
            return self.parse_subquery()
        else:
            raise Exception(f"Unexpected token in expression: {current_token}")

    def parse_subquery(self) -> Subquery:
        """
        Parses a subquery in the WHERE clause.

        :return: An ASTNode representing the parsed subquery.
        """
        # self.parser.consume('PUNCTUATION', '(')
        # subquery = self.parse_query()
        # self.parser.consume('PUNCTUATION', ')')
        raise NotImplementedError

    def parse_identifier(self) -> Identifier:
        """
        Parses an identifier from the current token stream.

        :return: An Identifier object representing the parsed identifier.
        """
        identifier = self.parser.consume("IDENTIFIER").value
        if (
            self.parser.current_token()
            and self.parser.current_token().type == "PUNCTUATION"
            and self.parser.current_token().value == "."
        ):
            self.parser.consume("PUNCTUATION", ".")
            identifier += "." + self.parser.consume("IDENTIFIER").value
        return Identifier(identifier)

    def parse_condition(self) -> ASTNode:
        """
        Parses a condition in the WHERE clause.

        This function starts by parsing a boolean factor (e.g., a simple condition) using the `parse_boolean_factor` method.
        It then checks for specific keywords like IS, BETWEEN, and LIKE in the current token stream.
        If a keyword is found, it calls the corresponding parsing method (`parse_is_null`, `parse_between_clause`, or `parse_like_clause`)
        and returns the result.

        If no specific keyword is found, it checks for comparison operators like =, <, >, etc.
        If a comparison operator is found, it consumes the operator token and parses the right-hand side of the comparison
        using the `parse_boolean_factor` method. It then creates a `Comparison` node with the left-hand side, operator, and right-hand side.

        After handling comparison operators, the function checks for logical operators (AND, OR) in the current token stream.
        If a logical operator is found, it consumes the operator token and recursively calls this method to parse the right-hand side condition.
        It then creates a `LogicalOperation` node with the left-hand side, operator, and right-hand side.

        The function continues this process until no more logical operators are found or the end of the token stream is reached.
        It finally returns the parsed condition.

        :return: An ASTNode representing the parsed condition.
        """
        # Start by parsing a boolean factor (e.g., a simple condition)
        left = self.parse_boolean_factor()

        # Check for specific keywords like IS, BETWEEN, and other operations
        current_token = self.parser.current_token()
        if current_token is not None and current_token.type == "KEYWORD":
            if current_token.value.upper() == "IS":
                return self.parse_is_null(left)
            elif current_token.value.upper() == "BETWEEN":
                return self.parse_between_clause(left)
            elif current_token.value.upper() == "LIKE":
                return self.parse_like_clause(left)

        # Handle comparison operators (e.g., =, <, >, etc.)
        if current_token is not None and current_token.type == "OPERATOR":
            operator = self.parser.consume("OPERATOR").value
            right = self.parse_boolean_factor()
            left = Comparison(left, Operator(operator), right)

        # Handle logical operators (AND, OR)
        while current_token is not None and current_token.type == "KEYWORD":
            if current_token.value.upper() == "AND":
                self.parser.consume("KEYWORD", "AND")
                right = self.parse_condition()
                left = LogicalOperation(left, "AND", right)
            elif current_token.value.upper() == "OR":
                self.parser.consume("KEYWORD", "OR")
                right = self.parse_condition()
                left = LogicalOperation(left, "OR", right)
            else:
                break

            # Update current_token after consumption
            current_token = self.parser.current_token()

        return left

    def parse_like_clause(self, left: ASTNode) -> ASTNode:
        """
        Parses a LIKE clause in the WHERE condition.

        :param left: The left-hand side of the LIKE clause, represented as an ASTNode.
        :return: An ASTNode representing the parsed LIKE clause.
        """
        self.parser.consume("KEYWORD", "LIKE")
        right = self.parser.consume("STRING").value  # Assuming the pattern is a string literal
        return Comparison(left, Operator("LIKE"), Literal(right))

    def parse_boolean_factor(self) -> ASTNode:
        """
        Parses a boolean factor from the token stream.

        This function checks for various conditions such as boolean literals, IN clauses, and logical operations.
        It recursively parses boolean terms and combines them using logical operations.

        :return: An ASTNode representing the parsed boolean factor.
        """
        current_token = self.parser.current_token()

        # Use the parse_boolean_literal function if a boolean is detected
        if current_token is not None and current_token.type == "BOOLEAN":
            return self.parse_boolean_literal()

        # Check for IN clause first
        if current_token is not None and current_token.type == "IDENTIFIER":
            next_token = self.parser.peek_token()
            if next_token and next_token.type == "KEYWORD" and next_token.value.upper() == "IN":
                return self.parse_in_clause()

        left = self.parse_boolean_term()

        while (
            current_token is not None
            and current_token.type == "KEYWORD"
            and current_token.value.upper() == "AND"
        ):
            self.parser.consume("KEYWORD", "AND")
            right = self.parse_boolean_term()
            left = LogicalOperation(left, "AND", right)

            current_token = self.parser.current_token()

        return left

    def parse_boolean_term(self) -> ASTNode:
        """
        Parses a boolean term from the token stream.

        This function checks for various conditions such as negation, parentheses, and comparisons.
        It recursively parses conditions and comparisons, and returns an ASTNode representing the parsed boolean term.

        :return: An ASTNode representing the parsed boolean term.
        """
        if (
            self.parser.current_token()
            and self.parser.current_token().type == "KEYWORD"
            and self.parser.current_token().value.upper() == "NOT"
        ):
            self.parser.consume("KEYWORD", "NOT")
            return UnaryOperation("NOT", self.parse_boolean_term())
        elif (
            self.parser.current_token()
            and self.parser.current_token().type == "PUNCTUATION"
            and self.parser.current_token().value == "("
        ):
            self.parser.consume("PUNCTUATION", "(")
            condition = self.parse_condition()
            self.parser.consume("PUNCTUATION", ")")
            return condition
        else:
            return self.parse_comparison()

    def parse_in_clause(self) -> InList:
        """
        Parses an IN clause in a SQL query.

        This function consumes the 'IN' keyword and the opening and closing parentheses.
        It then parses the expression before the 'IN' keyword and the values inside the IN clause.

        Returns:
            An InList object representing the parsed IN clause.

        Raises:
            ValueError: If the current token is not the 'IN' keyword.

        """
        # Parse the expression before the IN keyword
        expression = self.parse_expression()  # Parse the column or expression

        # Consume 'IN' keyword
        self.parser.consume("KEYWORD", "IN")

        # Consume '('
        self.parser.consume("PUNCTUATION", "(")

        # Parse the values inside the IN clause
        values = []
        while True:
            # Parse each value (could be a Literal or Identifier)
            value = self.parse_expression()  # Assume this method handles literals and identifiers
            values.append(value)

            # Check if the next token is a comma, indicating more values
            if (
                self.parser.current_token().type == "PUNCTUATION"
                and self.parser.current_token().value == ","
            ):
                self.parser.consume("PUNCTUATION", ",")
            else:
                break

        # Consume ')'
        self.parser.consume("PUNCTUATION", ")")

        # Create and return the InList node
        return InList(expression, values)

    def parse_logical_operation(self, conditions: List[ASTNode]) -> LogicalOperation:
        """
        Combines a list of conditions into a single logical operation.

        Args:
            conditions (List[ASTNode]): A list of conditions to be combined.

        Returns:
            LogicalOperation: The combined logical operation, or None if the input list is empty.
        """
        # Combine conditions into a single logical operation
        if not conditions:
            return None
        result = conditions[0]
        for i in range(1, len(conditions)):
            result = LogicalOperation(result, "AND", conditions[i])  # Example for 'AND'
        return result

    def parse_between_clause(self, expression: ASTNode) -> Between:
        """
        Parse a BETWEEN clause in the WHERE statement.

        Parameters:
            expression (ASTNode): The expression to be evaluated between two values.

        Returns:
            Between: A Between object containing the expression, lower bound, and upper bound.
        """
        # Handle the 'BETWEEN' clause
        self.parser.consume("KEYWORD", "BETWEEN")
        lower = self.parse_expression()
        self.parser.consume("KEYWORD", "AND")
        upper = self.parse_expression()

        return Between(expression, lower, upper)

    def parse_boolean_literal(self) -> ASTNode:
        """
        Parses a boolean literal from the current token.

        Args:
            None

        Returns:
            ASTNode: A BooleanLiteral node representing the parsed boolean value.
        """
        current_token = self.parser.current_token()

        if current_token is not None and current_token.type == "BOOLEAN":
            boolean_value = current_token.value.upper()
            self.parser.consume("BOOLEAN", boolean_value)
            return BooleanLiteral(boolean_value)
        raise SyntaxError("Expected a boolean literal ('TRUE' or 'FALSE').")

    def parse_is_null(self, expression: ASTNode) -> ASTNode:
        """
        Parses an 'IS NULL' or 'IS NOT NULL' clause in the WHERE statement.

        Parameters:
            expression (ASTNode): The expression to be evaluated for nullity.

        Returns:
            ASTNode: An IsNullOperation node representing the parsed 'IS NULL' or 'IS NOT NULL' clause.
        """
        self.parser.consume("KEYWORD", "IS")
        next_token = self.parser.current_token()

        if next_token is not None and next_token.type == "KEYWORD":
            if next_token.value.upper() == "NOT":
                self.parser.consume("KEYWORD", "NOT")
                null_token = self.parser.current_token()
                if (
                    null_token is not None
                    and null_token.type == "KEYWORD"
                    and null_token.value.upper() == "NULL"
                ):
                    self.parser.consume("KEYWORD", "NULL")
                    return IsNullOperation(expression=expression, negation=True)
                raise SyntaxError("Expected 'NULL' after 'IS NOT'.")
            elif next_token.value.upper() == "NULL":
                self.parser.consume("KEYWORD", "NULL")
                return IsNullOperation(expression=expression, negation=False)
            else:
                raise SyntaxError("Expected 'NULL' or 'NOT NULL' after 'IS'.")
        else:
            raise SyntaxError("Expected 'NULL' or 'NOT NULL' after 'IS'.")
