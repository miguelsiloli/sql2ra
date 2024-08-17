from ..primitives.ast_base import ASTNode
from .clauses import (
    SelectClause,
    FromClause,
    WhereClause,
    GroupByClause,
    OrderByClause,
    JoinClause,
    HavingClause,
)
from typing import Optional, List


class Query(ASTNode):
    """
    Represents an SQL query.

    The Query class encapsulates the various clauses of an SQL query, including
    SELECT, FROM, WHERE, JOIN, ORDER BY, GROUP BY, and HAVING. It organizes these
    components into an abstract syntax tree (AST) for further processing or analysis.

    :param select_clause: The SELECT clause of the query, represented by a SelectClause object.
    :param from_clause: The FROM clause of the query, represented by a FromClause object.
    :param where_clause: An optional WHERE clause of the query, represented by a WhereClause object.
    :param join_clauses: An optional list of JOIN clauses, each represented by a JoinClause object.
    :param order_by_clause: An optional ORDER BY clause, represented by an OrderByClause object.
    :param group_by_clause: An optional GROUP BY clause, represented by a GroupByClause object.
    :param having_clause: An optional HAVING clause, represented by a HavingClause object.
    """

    def __init__(
        self,
        select_clause: SelectClause,
        from_clause: FromClause,
        where_clause: Optional[WhereClause] = None,
        join_clauses: Optional[List[JoinClause]] = None,
        order_by_clause: Optional[OrderByClause] = None,
        group_by_clause: Optional[GroupByClause] = None,
        having_clause: Optional[HavingClause] = None,
    ):
        """
        Initializes the Query instance with the various SQL clauses.

        The constructor sets up the SQL query by organizing the provided clauses
        into an abstract syntax tree (AST). If some clauses are not provided,
        they are set to None or an empty list by default.

        :param select_clause: The SELECT clause of the query, represented by a SelectClause object.
        :param from_clause: The FROM clause of the query, represented by a FromClause object.
        :param where_clause: An optional WHERE clause of the query, represented by a WhereClause object.
        :param join_clauses: An optional list of JOIN clauses, each represented by a JoinClause object.
        :param order_by_clause: An optional ORDER BY clause, represented by an OrderByClause object.
        :param group_by_clause: An optional GROUP BY clause, represented by a GroupByClause object.
        :param having_clause: An optional HAVING clause, represented by a HavingClause object.
        """
        super().__init__(
            "Query",
            [
                select_clause,
                from_clause,
                where_clause,
                join_clauses,
                order_by_clause,
                group_by_clause,
                having_clause,
            ],
        )
        self.select_clause = select_clause
        self.from_clause = from_clause
        self.where_clause = where_clause
        self.join_clauses = join_clauses or []
        self.order_by_clause = order_by_clause
        self.group_by_clause = group_by_clause
        self.having_clause = having_clause

    def __repr__(self):
        """
        Returns a string representation of the Query instance.

        The string includes all the major clauses of the query, making it useful for
        debugging and logging.

        :return: A string representation of the Query instance.
        """
        return (
            f"Query(select_clause={self.select_clause}, from_clause={self.from_clause}, "
            f"where_clause={self.where_clause}, join_clauses={self.join_clauses}, "
            f"group_by_clause={self.group_by_clause}, having_clause={self.having_clause}), "
            f"order_by_clause={self.order_by_clause}"
        )

    def to_dict(self) -> dict:
        """
        Converts the Query instance to a dictionary representation.

        This method recursively converts all the clauses of the query to dictionaries,
        enabling easy serialization or further processing.

        :return: A dictionary representation of the Query instance.
        """
        return {
            "node_type": "Query",
            "select_clause": self.select_clause.to_dict(),
            "from_clause": self.from_clause.to_dict(),
            "where_clause": self.where_clause.to_dict() if self.where_clause else None,
            "join_clauses": [join_clause.to_dict() for join_clause in self.join_clauses]
            if self.join_clauses
            else [],
            "group_by_clause": self.group_by_clause.to_dict() if self.group_by_clause else None,
            "having_clause": self.having_clause.to_dict() if self.having_clause else None,
            "order_by_clause": self.order_by_clause.to_dict() if self.order_by_clause else None,
        }
