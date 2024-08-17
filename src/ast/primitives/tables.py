from .ast_base import ASTNode
from typing import Optional
import re


class Table(ASTNode):
    """
    Represents a table in an SQL query.

    The Table class is used to represent a table in the FROM clause of an SQL query.
    It supports handling table aliases and can parse the table name and alias from
    a string of the form "table_name AS alias".

    :param name: The name of the table.
    :param alias: An optional alias for the table.
    """

    def __init__(self, name: str, alias: Optional[str] = None):
        """
        Initializes the Table instance with a name and an optional alias.

        If the name is provided in the form "table_name AS alias", the name and alias
        are automatically extracted. If the alias is provided separately, it is stored
        as the alias for the table.

        :param name: The name of the table, potentially including an alias (e.g., "table_name AS alias").
        :param alias: An optional alias for the table.
        """
        # Split name and alias if provided in the form "name AS alias"
        match = re.match(r"(\w+)\s+AS\s+(\w+)", name, re.IGNORECASE)
        if match:
            self.name = match.group(1)
            self.alias = match.group(2)
        else:
            self.name = name
            self.alias = alias

    def __repr__(self):
        """
        Returns a string representation of the Table instance.

        :return: A string in the format "Table(name='table_name', alias=alias)".
        """
        return f"Table(name='{self.name}', alias={self.alias})"

    def to_dict(self) -> dict:
        """
        Converts the Table instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "Table", "name": "table_name", "alias": "alias"}.
                 The "alias" key is only included if an alias is present.
        """
        result = {"node_type": "Table", "name": self.name}
        if self.alias:
            result["alias"] = self.alias
        return result


class DerivedTable(ASTNode):
    """
    Represents a derived table (subquery) in an SQL query.

    The DerivedTable class is used to represent a subquery within the FROM clause
    of an SQL query. It includes the subquery itself and an optional alias.

    :param subquery: An ASTNode representing the subquery.
    :param alias: An optional alias for the derived table.
    """

    def __init__(self, subquery: ASTNode, alias: Optional[str] = None):
        """
        Initializes the DerivedTable instance with a subquery and an optional alias.

        :param subquery: An ASTNode representing the subquery.
        :param alias: An optional alias for the derived table.
        """
        self.subquery = subquery
        self.alias = alias

    def __repr__(self):
        """
        Returns a string representation of the DerivedTable instance.

        :return: A string in the format "DerivedTable(subquery=subquery_repr, alias=alias)".
        """
        return f"DerivedTable(subquery={self.subquery}, alias={self.alias})"

    def to_dict(self) -> dict:
        """
        Converts the DerivedTable instance to a dictionary representation.

        :return: A dictionary with the structure {"node_type": "DerivedTable", "subquery": subquery_dict, "alias": "alias"}.
                 The "alias" key is only included if an alias is present.
        """
        result = {
            "node_type": "DerivedTable",
            "subquery": self.subquery.to_dict(),  # Assuming subquery has its own to_dict
        }
        if self.alias:
            result["alias"] = self.alias
        return result
