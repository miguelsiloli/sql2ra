from ..primitives import *
from ..derived_types import *


class FromParser:
    """
    A parser for the FROM clause in an SQL statement.

    The FromParser class is responsible for parsing the FROM clause, which
    specifies the tables or subqueries from which the data is selected.
    It supports parsing both regular tables and derived tables (subqueries).
    """

    def __init__(self, parser):
        """
        Initializes the FromParser with a Parser instance.

        :param parser: An instance of the Parser class used for token consumption and lookahead.
        """
        self.parser = parser
        # self.select_parser = select_parser  # Uncomment or define if SelectParser is needed

    def parse_subquery(self):
        """
        Parses a subquery within the FROM clause.

        This method is a placeholder and should be implemented to handle
        subqueries in the FROM clause. Subqueries are typically enclosed
        in parentheses and can be aliased.

        :raise NotImplementedError: This method is not yet implemented.
        """
        raise NotImplementedError

    def parse_from(self) -> FromClause:
        """
        Parses the FROM clause of an SQL statement.

        This method consumes the FROM keyword and then iterates through the
        tokens to identify tables or subqueries specified in the FROM clause.
        It handles table aliases and multiple tables separated by commas.

        :return: A FromClause object representing the parsed FROM clause.
        """
        self.parser.consume("KEYWORD", "FROM")
        tables = []

        while True:
            current_token = self.parser.current_token()

            if current_token is None:
                break  # Exit the loop if there are no more tokens to process

            if current_token.type == "PUNCTUATION" and current_token.value == "(":
                # Handle subqueries
                subquery = self.parse_subquery()
                alias = None
                if self.parser.current_token() and self.parser.current_token().type == "IDENTIFIER":
                    alias = self.parser.consume("IDENTIFIER").value
                tables.append(DerivedTable(subquery, alias))
            else:
                # Handle regular tables
                table_name = self.parser.consume("IDENTIFIER").value
                alias = None
                if self.parser.current_token() and self.parser.current_token().type == "IDENTIFIER":
                    alias = self.parser.consume("IDENTIFIER").value
                tables.append(Table(table_name, alias))

            current_token = self.parser.current_token()
            if current_token and current_token.type == "PUNCTUATION" and current_token.value == ",":
                self.parser.consume("PUNCTUATION", ",")
            else:
                break

        return FromClause(tables)
