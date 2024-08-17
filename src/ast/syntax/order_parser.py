from ..derived_types import Identifier, Order, OrderByClause
from typing import Optional


class OrderByParser:
    """
    A parser for the ORDER BY clause in an SQL query.

    The OrderByParser class is responsible for parsing the ORDER BY clause,
    which specifies the order in which the result set should be returned.
    This parser extracts the columns or expressions and their corresponding
    sorting order (ASC or DESC) specified in the clause.
    """

    def __init__(self, parser):
        """
        Initializes the OrderByParser with a reference to the main parser.

        :param parser: The main SQL parser object that provides the token stream
                       and utility methods for token consumption and lookahead.
        """
        self.parser = parser

    def parse_order_by(self) -> Optional[OrderByClause]:
        """
        Parses the ORDER BY clause of an SQL query.

        This method checks if the current tokens represent an ORDER BY clause,
        and if so, it processes each column or expression listed in the clause,
        determining the sorting order (ASC or DESC) for each. The parsed result
        is returned as an OrderByClause object.

        :return: An OrderByClause object containing the list of columns or expressions
                 and their respective sorting order, or None if no ORDER BY clause is found.
        """
        if (
            self.parser.current_token()
            and self.parser.current_token().type == "KEYWORD"
            and self.parser.current_token().value.upper() == "ORDER BY"
        ):
            self.parser.consume("KEYWORD", "ORDER BY")
            order_by_items = []

            while self.parser.current_token() and self.parser.current_token().type == "IDENTIFIER":
                identifier = self.parser.consume("IDENTIFIER").value
                if self.parser.current_token() and self.parser.current_token().value == ".":
                    self.parser.consume("PUNCTUATION", ".")
                    identifier += "." + self.parser.consume("IDENTIFIER").value

                column = Identifier(identifier)
                order = None  # Default order is None

                # Check for ASC or DESC keyword
                if self.parser.current_token() and self.parser.current_token().type == "KEYWORD":
                    order_token = self.parser.current_token().value.upper()
                    if order_token in ["ASC", "DESC"]:
                        order = self.parser.consume("KEYWORD", order_token).value.upper()

                order_by_items.append(Order(column, order))

                if self.parser.current_token() and self.parser.current_token().value == ",":
                    self.parser.consume("PUNCTUATION", ",")
                else:
                    break

            return OrderByClause(order_by_items)

        return None
