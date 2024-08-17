from ..primitives import *
from ..derived_types import SelectClause, SelectItem, Wildcard, FunctionCall, Identifier

"""
1. Basic Column Selection
Case: SELECT column_name
Example: SELECT a.id
Action: Parse the identifier a.id and add it to the SelectClause.

2. Column with Alias
Case: SELECT column_name AS alias
Example: SELECT a.name AS employee_name
Action: Parse the identifier a.name and the alias employee_name, then add them to the SelectClause.

3. Function Call
Case: SELECT FUNCTION_NAME(arguments)
Example: SELECT COUNT(*)
Action: Parse the function COUNT with its argument * and add it to the SelectClause.

4. Function Call with Alias
Case: SELECT FUNCTION_NAME(arguments) AS alias
Example: SELECT COUNT(*) AS total_count
Action: Parse the function COUNT with its argument * and the alias total_count, then add them to the SelectClause.

5. Multiple Columns
Case: SELECT column1, column2
Example: SELECT a.id, b.name
Action: Parse multiple identifiers and add them to the SelectClause, handling each comma-separated item.

6. Mixed Columns and Functions
Case: SELECT column_name, FUNCTION_NAME(arguments)
Example: SELECT a.id, COUNT(*)
Action: Parse a combination of identifiers and functions, adding each to the SelectClause.

7. Column with Complex Identifiers
Case: SELECT table.column
Example: SELECT a.department_id
Action: Parse complex identifiers with table.column notation.

8. Function with Multiple Arguments
Case: SELECT FUNCTION_NAME(arg1, arg2)
Example: SELECT SUM(salary), MAX(age)
Action: Parse functions with multiple arguments and add them to the SelectClause.

9. Empty SELECT Clause
Case: SELECT *
Example: SELECT *
Action: Handle the wildcard * correctly, representing it as a special case in the SelectClause.
"""


class SelectParser:
    """
    A parser for the SELECT clause in an SQL statement.

    The SelectParser class is responsible for parsing the SELECT clause,
    including handling column identifiers, function calls, wildcards,
    and aliases. It processes each item in the SELECT clause and returns
    a structured representation of the clause.
    """

    def __init__(self, parser):
        """
        Initializes the SelectParser with a Parser instance.

        :param parser: An instance of the Parser class used for token
                       consumption and lookahead during parsing.
        """
        self.parser = parser

    def parse_select(self) -> SelectClause:
        """
        Parses the SELECT clause of an SQL statement.

        This method consumes the SELECT keyword, then iterates through
        the columns, function calls, or wildcards in the SELECT clause.
        It handles aliases and ensures proper structure in the resulting
        SelectClause object.

        :return: A SelectClause object representing the parsed SELECT clause.
        """
        self.parser.consume("KEYWORD", "SELECT")
        columns = []

        while True:
            current_token = self.parser.current_token()

            # Exit condition if a keyword that signals the end of the SELECT clause is encountered
            if current_token.type == "KEYWORD" and current_token.value.upper() in {
                "FROM",
                "WHERE",
                "JOIN",
                "GROUP BY",
                "HAVING",
                "ORDER BY",
            }:
                break

            if current_token.type == "WILDCARD":
                # Handle wildcard '*'
                columns.append(SelectItem(Wildcard(), None))
                self.parser.consume("WILDCARD")

            elif (
                current_token.type == "KEYWORD"
                and self.parser.peek_token()
                and self.parser.peek_token().type == "PUNCTUATION"
                and self.parser.peek_token().value == "("
            ):
                # Handle function calls where the function name is a keyword
                function = self.parse_function()
                alias = self.parse_alias()
                columns.append(SelectItem(function, alias))

            elif current_token.type == "IDENTIFIER":
                # Handle normal columns
                column = self.parse_identifier()
                alias = self.parse_alias()
                columns.append(SelectItem(column, alias))
            else:
                raise ValueError(
                    f"Unexpected token type: {current_token.type}, value: {current_token.value}"
                )

            # Check if there's a comma to continue parsing, otherwise break
            current_token = (
                self.parser.current_token()
            )  # Re-fetch current token after potential consumption
            if current_token.type == "PUNCTUATION" and current_token.value == ",":
                self.parser.consume("PUNCTUATION", ",")
            else:
                break

        return SelectClause(columns)

    def parse_function(self) -> FunctionCall:
        """
        Parses a function call in the SELECT clause.

        This method expects a keyword representing the function name,
        consumes the function name and parentheses, and then processes
        the arguments within the function call.

        :return: A FunctionCall object representing the parsed function call.
        """
        current_token = self.parser.current_token()

        if current_token.type != "KEYWORD":
            raise ValueError(
                f"Tried to parse function keyword but got identifier: {current_token.value}"
            )

        function_name = self.parser.consume("KEYWORD").value
        self.parser.consume("PUNCTUATION", "(")
        arguments = []

        while self.parser.current_token() and (
            self.parser.current_token().type != "PUNCTUATION"
            or self.parser.current_token().value != ")"
        ):
            current_token = self.parser.current_token()

            if current_token.type == "WILDCARD":
                # Handle wildcard '*' as a valid argument
                arg = Wildcard()
                self.parser.consume("WILDCARD")
            elif current_token.type == "IDENTIFIER":
                arg = self.parse_identifier()  # Adjust to your argument parsing logic
            else:
                raise ValueError(
                    f"Unexpected token type {current_token.type} in function arguments"
                )

            arguments.append(arg)

            if (
                self.parser.current_token()
                and self.parser.current_token().type == "PUNCTUATION"
                and self.parser.current_token().value == ","
            ):
                self.parser.consume("PUNCTUATION", ",")

        self.parser.consume("PUNCTUATION", ")")
        return FunctionCall(function_name, arguments)

    def parse_alias(self) -> Optional[str]:
        """
        Parses an alias for a column or function in the SELECT clause.

        This method checks if the next keyword is 'AS', and if so, it consumes
        the alias identifier following 'AS'. If no alias is present, it returns None.

        :return: The alias as a string if present, otherwise None.
        """
        if (
            self.parser.current_token()
            and self.parser.current_token().type == "KEYWORD"
            and self.parser.current_token().value.upper() == "AS"
        ):
            self.parser.consume("KEYWORD", "AS")
            return self.parser.consume("IDENTIFIER").value
        return None

    def parse_identifier(self) -> Identifier:
        """
        Parses an identifier, which could represent a column name, table name, or field.

        This method consumes an identifier and checks if it is part of a
        qualified name (e.g., table.column). If so, it concatenates the parts
        to form the full identifier.

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
