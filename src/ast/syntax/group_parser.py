from ..primitives import *
from ..derived_types import *


class GroupByParser:
    """
    A parser for the GROUP BY clause in an SQL statement.

    The GroupByParser class is responsible for parsing the GROUP BY clause,
    including handling multiple columns specified for grouping. It constructs
    a structured representation of the GROUP BY clause.
    """

    def __init__(self, parser):
        """
        Initializes the GroupByParser with a Parser instance.

        :param parser: An instance of the Parser class used for token consumption and lookahead.
        """
        self.parser = parser

    def parse_group_by(self) -> Optional[GroupByClause]:
        """
        Parses the GROUP BY clause of an SQL statement if it exists.

        This method checks for the presence of the 'GROUP BY' keywords and
        processes the columns specified for grouping. It returns a GroupByClause
        object representing the parsed GROUP BY clause or None if the clause
        is not present.

        :return: A GroupByClause object representing the parsed GROUP BY clause, or None if the clause is not present.
        """
        # Check if the current token is 'GROUP' and the next token is 'BY'
        if (
            self.parser.current_token()
            and self.parser.current_token().type == "KEYWORD"
            and self.parser.current_token().value.upper() == "GROUP BY"
        ):
            self.parser.consume("KEYWORD", "GROUP BY")
        else:
            # If 'GROUP BY' is not present, return None or handle appropriately
            return None

        columns = []

        while True:
            # Parse the identifier for the group by column
            column = self.parse_identifier()
            columns.append(column)

            # Check if there are more columns to group by
            if (
                self.parser.current_token()
                and self.parser.current_token().type == "PUNCTUATION"
                and self.parser.current_token().value == ","
            ):
                self.parser.consume("PUNCTUATION", ",")
            else:
                break

        return GroupByClause(columns)

    def parse_identifier(self) -> Identifier:
        """
        Parses an identifier, which could be a column name, table name, or field.

        This method consumes an identifier token and handles qualified names
        (e.g., table.column). It returns an Identifier object representing
        the parsed identifier.

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
