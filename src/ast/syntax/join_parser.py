from ..primitives import *
from ..derived_types import *
from typing import List


class JoinParser:
    def __init__(self, parser):
        """
        Initializes a JoinParser object with a parser.

        Parameters:
        parser (object): The parser object to be used by the JoinParser.

        Returns:
        None
        """
        self.parser = parser

    def parse_joins(self) -> List[JoinClause]:
        """
        Parses a series of join clauses and returns a list of JoinClause objects.

        This method consumes tokens from the parser until it encounters a token that is not a keyword or does not contain the word 'JOIN'.
        Each join clause consists of a join type, a table reference, an optional alias, an ON keyword, a comparison between two identifiers, and an optional alias.
        The method creates and appends a JoinClause object to the list for each join clause parsed.

        :return: A list of JoinClause objects representing the parsed join clauses.
        """
        joins = []

        while (
            self.parser.current_token()
            and self.parser.current_token().type == "KEYWORD"
            and "JOIN" in self.parser.current_token().value.upper()
        ):
            join_type = self.parser.consume("KEYWORD").value.upper()

            # Ensure that the next token is an IDENTIFIER (table reference)
            table_reference_token = self.parser.consume("IDENTIFIER").value
            alias = None

            # Handle optional alias
            if " AS " in table_reference_token.upper():
                table_name, alias = map(str.strip, table_reference_token.split(" AS ", 1))
            else:
                table_name = table_reference_token

            # Check if the next token is a separate alias
            current_token = self.parser.current_token()
            if current_token and current_token.type == "IDENTIFIER":
                alias = self.parser.consume("IDENTIFIER").value

            # Expect and consume the ON keyword
            self.parser.consume("KEYWORD", "ON")

            # Parse the left side of the comparison
            left = self.parser.consume("IDENTIFIER").value
            current_token = self.parser.current_token()
            if current_token and current_token.type == "PUNCTUATION" and current_token.value == ".":
                self.parser.consume("PUNCTUATION", ".")
                left += "." + self.parser.consume("IDENTIFIER").value

            # Parse the operator (e.g., =)
            operator = self.parser.consume("OPERATOR").value

            # Parse the right side of the comparison
            right = self.parser.consume("IDENTIFIER").value
            current_token = self.parser.current_token()
            if current_token and current_token.type == "PUNCTUATION" and current_token.value == ".":
                self.parser.consume("PUNCTUATION", ".")
                right += "." + self.parser.consume("IDENTIFIER").value

            # Create and append the JoinClause
            joins.append(
                JoinClause(
                    join_type,
                    TableReference(table_name, alias),
                    Comparison(Identifier(left), Operator(operator), Identifier(right)),
                )
            )

            # Move to the next token after processing the join
            current_token = self.parser.current_token()
            if not current_token or "JOIN" not in current_token.value.upper():
                break

        return joins
