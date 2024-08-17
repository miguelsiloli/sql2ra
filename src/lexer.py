from typing import List, NamedTuple
import sqlparse
from sqlparse.sql import Token as SqlparseToken
from sqlparse.tokens import Token as SqlparseTokenType


class Token(NamedTuple):
    type: str
    value: str


def tokenize(sql_string: str) -> List[Token]:
    """
    Tokenizes the input SQL string into a list of tokens.

    Args:
        sql_string (str): SQL query string.

    Returns:
        List[Token]: List of tokens with their types and values.
    """
    # Parse the SQL string
    parsed = sqlparse.parse(sql_string)[0]

    # Initialize the list to store our custom Token objects
    tokens = []

    # Flatten the token stream and convert to our custom Token objects
    for token in parsed.flatten():
        # Map sqlparse token types to more general categories
        token_type = map_token_type(token.ttype)

        if token_type != "OTHER":
            tokens.append(Token(type=token_type, value=token.value))

    return tokens


def map_token_type(token):
    """
    Maps sqlparse token types to more general categories.
    """
    ttype = token.ttype
    value = token.value

    if ttype in SqlparseTokenType.Keyword or value in ("COUNT", "SUM", "AVG", "MIN", "MAX"):
        return "KEYWORD"
    elif ttype in SqlparseTokenType.DML:
        return "DML"
    elif ttype in SqlparseTokenType.DDL:
        return "DDL"
    elif ttype in SqlparseTokenType.Name:
        return "IDENTIFIER"
    elif ttype in SqlparseTokenType.Literal:
        return "LITERAL"
    elif ttype in SqlparseTokenType.Operator:
        return "OPERATOR"
    elif ttype in SqlparseTokenType.Punctuation:
        return "PUNCTUATION"
    elif ttype in SqlparseTokenType.Wildcard:
        return "WILDCARD"
    elif ttype in SqlparseTokenType.Comment:
        return "COMMENT"
    elif token.upper() in ("TRUE", "FALSE"):
        return Token(type="BOOLEAN", value=token)
    else:
        return "OTHER"
