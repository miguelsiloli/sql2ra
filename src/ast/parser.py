from typing import List
from src.lexer import Token
from .primitives import ASTNode
from .derived_types import (
    SelectClause,
    FromClause,
    WhereClause,
    JoinClause,
    OrderByClause,
    GroupByClause,
    Query,
)
from .syntax import *

from typing import List, Optional

# Token and ASTNode definitions would be here


class Parser:
    def __init__(self, tokens: List[Token], debug=True):
        """
        Initializes the Parser with a list of tokens and sets the starting position.

        :param tokens: A list of Token objects representing the SQL query.
        """
        self.tokens = tokens
        self.position = 0
        self.debug = debug

    def consume(self, expected_type=None, expected_value=None) -> Token:
        """
        Consumes the current token and advances the position. If the current token does not match
        the expected type or value, a ValueError is raised.

        :param expected_type: The expected type of the token (e.g., 'KEYWORD', 'IDENTIFIER').
        :param expected_value: The expected value of the token (e.g., 'SELECT', 'FROM').
        :return: The consumed Token object.
        :raises ValueError: If the token does not match the expected type or value.
        """
        token = self.tokens[self.position]
        if expected_type and token.type != expected_type:
            # print("Select clause doesn't support nested Function calls. Example: Round(AVG(salary))")
            # print("Select clause doesn't support composite functions such as: CONCAT(first_name, ' ', last_name), SUBSTR(name, 1, 3), COALESCE, EXTRACT")
            # print("From clause does not support subqueries.")
            raise ValueError(f"Expected token ({token}) type {expected_type}, got {token.type}")
        if expected_value and token.value != expected_value:
            raise ValueError(f"Expected token value {expected_value}, got {token.value}")
        self.position += 1
        if self.debug:
            print(f"Consuming token {token}")
        return token

    def current_token(self) -> Optional[Token]:
        """
        Returns the current token without advancing the position.

        :return: The current Token object, or None if the end of the token list is reached.
        """
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def peek_token(self) -> Optional[Token]:
        """
        Returns the next token without advancing the position.

        :return: The next Token object, or None if there are no more tokens.
        """
        return self.tokens[self.position + 1] if (self.position + 1) < len(self.tokens) else None

    def select_parser(self) -> SelectClause:
        """
        Parses the SELECT clause of the SQL query.

        :return: A SelectClause object representing the parsed SELECT clause.
        """
        return SelectParser(self).parse_select()

    def from_parser(self) -> FromClause:
        """
        Parses the FROM clause of the SQL query.

        :return: A FromClause object representing the parsed FROM clause.
        """
        return FromParser(self).parse_from()

    def where_parser(self) -> WhereClause:
        """
        Parses the WHERE clause of the SQL query.

        :return: A WhereClause object representing the parsed WHERE clause.
        """
        return WhereParser(self).parse_where()

    def join_parser(self) -> List[JoinClause]:
        """
        Parses the JOIN clauses of the SQL query.

        :return: A list of JoinClause objects representing the parsed JOIN clauses.
        """
        return JoinParser(self).parse_joins()

    def parse(self) -> ASTNode:
        """
        Parses the entire SQL query by identifying and parsing each clause in sequence.

        :return: A Query object representing the entire parsed SQL query.
        """
        select_clause = None
        from_clause = None
        join_clause = None
        where_clause = None
        group_by_clause = None
        having_clause = None
        order_by_clause = None

        while self.current_token():
            token = self.current_token()

            if token.type == "KEYWORD":
                keyword = token.value.upper()

                if keyword == "SELECT":
                    select_clause = SelectParser(self).parse_select()

                elif keyword == "FROM":
                    from_clause = FromParser(self).parse_from()

                elif keyword == "JOIN" or keyword in (
                    "INNER JOIN",
                    "LEFT JOIN",
                    "RIGHT JOIN",
                    "FULL JOIN",
                ):
                    join_clause = JoinParser(self).parse_joins()

                elif keyword == "WHERE":
                    where_clause = WhereParser(self).parse_where()

                elif keyword == "GROUP BY":
                    group_by_clause = GroupByParser(self).parse_group_by()

                elif keyword == "HAVING":
                    having_clause = HavingClauseParser(self).parse_having()

                elif keyword == "ORDER BY":
                    order_by_clause = OrderByParser(self).parse_order_by()

                else:
                    self.consume(token.type)  # Move to the next token

        return Query(
            select_clause,
            from_clause,
            where_clause,
            join_clause,
            order_by_clause,
            group_by_clause,
            having_clause,
        )
