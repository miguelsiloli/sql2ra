import pytest
from src.ast.parser import Parser
from src.ast.derived_types import SelectClause, FromClause, WhereClause, GroupByClause, HavingClause, OrderByClause, JoinClause, Query
from src.lexer import Token

# 1. Basic SELECT Queries

def test_simple_select():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1')
    ]
    parser = Parser(tokens)
    query = parser.parse()
    print(query.select_clause.children[0].expression)
    assert isinstance(query.select_clause, SelectClause)
    assert query.select_clause.children[0].expression.name == 'column1'
    assert query.from_clause.table[0].name == 'table1'

def test_select_with_multiple_columns():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='PUNCTUATION', value=','),
        Token(type='IDENTIFIER', value='column2'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1')
    ]
    parser = Parser(tokens)
    query = parser.parse()
    assert len(query.select_clause.children) == 2
    assert query.select_clause.children[0].expression.name == 'column1'
    assert query.select_clause.children[1].expression.name == 'column2'

def test_select_with_wildcard():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='WILDCARD', value='*'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1')
    ]
    parser = Parser(tokens)
    query = parser.parse()

    assert query.select_clause.children[0].expression.to_dict()["value"] == '*'
    assert query.from_clause.table[0].name == 'table1'


# 2. WHERE Clause

def test_simple_where_clause():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1'),
        Token(type='KEYWORD', value='WHERE'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='OPERATOR', value='='),
        Token(type='STRING', value="'value'")
    ]
    parser = Parser(tokens)
    query = parser.parse()

    # Assert that the WHERE clause is correctly parsed
    assert isinstance(query.where_clause, WhereClause)

    # Convert the WHERE clause to a dictionary
    where_dict = query.where_clause.condition[0].to_dict()

    # Define the expected dictionary structure
    expected_where_dict = {
        'node_type': 'Comparison',
        'left': {
            'node_type': 'Identifier',
            'name': 'column1'
        },
        'operator': '=',
        'right': {
            'node_type': 'Literal',
            'value': "'value'"
        }
    }

    # Assert that the parsed WHERE clause matches the expected structure
    assert where_dict == expected_where_dict

def test_where_clause_with_and_or():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1'),
        Token(type='KEYWORD', value='WHERE'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='OPERATOR', value='='),
        Token(type='STRING', value="'value'"),
        Token(type='KEYWORD', value='AND'),
        Token(type='IDENTIFIER', value='column2'),
        Token(type='OPERATOR', value='>'),
        Token(type='NUMBER', value='10')
    ]
    parser = Parser(tokens)
    query = parser.parse()

    # Assert the WHERE clause is correctly parsed
    assert isinstance(query.where_clause, WhereClause)

    # Convert the WHERE clause to a dictionary
    where_dict = query.where_clause.condition[0].to_dict()

    # Define the expected structure
    expected_where_dict = {
        'node_type': 'LogicalOperation',
        'left': {
            'node_type': 'Comparison',
            'left': {
                'node_type': 'Identifier',
                'name': 'column1'
            },
            'operator': '=',
            'right': {
                'node_type': 'Literal',
                'value': "'value'"
            }
        },
        'operator': 'AND',
        'right': {
            'node_type': 'Comparison',
            'left': {
                'node_type': 'Identifier',
                'name': 'column2'
            },
            'operator': '>',
            'right': {
                'node_type': 'Literal',
                'value': '10'
            }
        }
    }

    # Assert that the parsed WHERE clause matches the expected structure
    assert where_dict == expected_where_dict

# def test_where_clause_with_like():
#     tokens = [
#         Token(type='KEYWORD', value='SELECT'),
#         Token(type='IDENTIFIER', value='column1'),
#         Token(type='KEYWORD', value='FROM'),
#         Token(type='IDENTIFIER', value='table1'),
#         Token(type='KEYWORD', value='WHERE'),
#         Token(type='IDENTIFIER', value='column1'),
#         Token(type='KEYWORD', value='LIKE'),
#         Token(type='STRING', value="'%value%'")
#     ]
#     parser = Parser(tokens)
#     query = parser.parse()
#     assert isinstance(query.where_clause, WhereClause)
#     assert query.where_clause.conditions[0].left.name == 'column1'
#     assert query.where_clause.conditions[0].operator == 'LIKE'
#     assert query.where_clause.conditions[0].right.value == "'%value%'"

def test_where_clause_with_in():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1'),
        Token(type='KEYWORD', value='WHERE'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='KEYWORD', value='IN'),
        Token(type='PUNCTUATION', value='('),
        Token(type='STRING', value="'value1'"),
        Token(type='PUNCTUATION', value=','),
        Token(type='STRING', value="'value2'"),
        Token(type='PUNCTUATION', value=','),
        Token(type='STRING', value="'value3'"),
        Token(type='PUNCTUATION', value=')')
    ]
    parser = Parser(tokens)
    query = parser.parse()

    # Assert the WHERE clause is correctly parsed
    assert isinstance(query.where_clause, WhereClause)

    # Convert the WHERE clause to a dictionary
    where_dict = query.where_clause.condition[0].to_dict()

    # Define the expected structure
    expected_where_dict = {
        'node_type': 'InList',
        'expression': {
            'node_type': 'Identifier',
            'name': 'column1'
        },
        'values': [
            {'node_type': 'Literal', 'value': "'value1'"},
            {'node_type': 'Literal', 'value': "'value2'"},
            {'node_type': 'Literal', 'value': "'value3'"}
        ]
    }

    # Assert that the parsed WHERE clause matches the expected structure
    assert where_dict == expected_where_dict

def test_where_clause_with_between():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1'),
        Token(type='KEYWORD', value='WHERE'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='KEYWORD', value='BETWEEN'),
        Token(type='NUMBER', value='10'),
        Token(type='KEYWORD', value='AND'),
        Token(type='NUMBER', value='20')
    ]
    parser = Parser(tokens)
    query = parser.parse()

    # Assert the WHERE clause is correctly parsed
    assert isinstance(query.where_clause, WhereClause)

    # Convert the WHERE clause to a dictionary
    where_dict = query.where_clause.condition[0].to_dict()

    # Define the expected structure
    expected_where_dict = {
        'node_type': 'Between',
        'expression': {
            'node_type': 'Identifier',
            'name': 'column1'
        },
        'lower': {
            'node_type': 'Literal',
            'value': '10'
        },
        'upper': {
            'node_type': 'Literal',
            'value': '20'
        }
    }

    # Assert that the parsed WHERE clause matches the expected structure
    assert where_dict == expected_where_dict


def test_where_clause_with_is_null():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1'),
        Token(type='KEYWORD', value='WHERE'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='KEYWORD', value='IS'),
        Token(type='KEYWORD', value='NULL')
    ]
    parser = Parser(tokens)
    query = parser.parse()

    # Assert the WHERE clause is correctly parsed
    assert isinstance(query.where_clause, WhereClause)

    # Convert the WHERE clause to a dictionary
    where_dict = query.where_clause.condition[0].to_dict()

    # Define the expected structure
    expected_where_dict = {
        'node_type': 'IsNullOperation',
        'negation': False,
        'children': [
            {
                'node_type': 'Identifier',
                'name': 'column1'
            }
        ]
    }

    # Assert that the parsed WHERE clause matches the expected structure
    assert where_dict == expected_where_dict



# 3. ORDER BY Clause

def test_simple_order_by():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1'),
        Token(type='KEYWORD', value='ORDER BY'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='KEYWORD', value='ASC')
    ]
    parser = Parser(tokens)
    query = parser.parse()

    # Ensure the order_by_clause is an OrderByClause instance
    assert isinstance(query.order_by_clause, OrderByClause), f"Expected OrderByClause, got {type(query.order_by_clause)}"
    
    # Convert the OrderByClause to a dictionary to match the expected output
    order_by_dict = query.order_by_clause.to_dict()
    print(order_by_dict)

    # Perform assertions on the dictionary representation
    expected_order_by_dict = {
        "node_type": "OrderByClause",
        "children": [
            {
                "node_type": "Order",
                "column": {
                    "node_type": "Identifier",
                    "name": "column1"
                },
                "order": "ASC"
            }
        ]
    }

    # Assert the actual output matches the expected dictionary
    assert order_by_dict == expected_order_by_dict, f"Expected {expected_order_by_dict}, got {order_by_dict}"


def test_order_by_with_multiple_columns():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='PUNCTUATION', value=','),
        Token(type='IDENTIFIER', value='column2'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1'),
        Token(type='KEYWORD', value='ORDER BY'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='KEYWORD', value='DESC'),
        Token(type='PUNCTUATION', value=','),
        Token(type='IDENTIFIER', value='column2'),
        Token(type='KEYWORD', value='ASC')
    ]
    
    parser = Parser(tokens)
    query = parser.parse()
    
    # Convert the parsed query to a dictionary
    query_dict = query.to_dict()
    print(query_dict)
    
    # Expected dictionary structure
    expected_dict = {
        'node_type': 'Query',
        'select_clause': {
            'node_type': 'SelectClause',
            'children': [
                {
                    'node_type': 'SelectItem',
                    'children': [{'node_type': 'Identifier', 'name': 'column1'}],
                    'expression': {'node_type': 'Identifier', 'name': 'column1'}
                },
                {
                    'node_type': 'SelectItem',
                    'children': [{'node_type': 'Identifier', 'name': 'column2'}],
                    'expression': {'node_type': 'Identifier', 'name': 'column2'}
                }
            ]
        },
        'from_clause': {
            'node_type': 'FromClause',
            'table': {'node_type': 'Table', 'name': 'table1'}
        },
        'where_clause': None,
        'join_clauses': [],
        'group_by_clause': None,
        'having_clause': None,
        'order_by_clause': {
            'node_type': 'OrderByClause',
            'children': [
                {
                    'node_type': 'Order',
                    'column': {'node_type': 'Identifier', 'name': 'column1'},
                    'order': 'DESC'
                },
                {
                    'node_type': 'Order',
                    'column': {'node_type': 'Identifier', 'name': 'column2'},
                    'order': 'ASC'
                }
            ]
        }
    }

    # Compare the parsed dictionary with the expected dictionary
    assert query_dict == expected_dict, (
        f"Expected: {expected_dict}, but got: {query_dict}"
    )


# 4. GROUP BY and HAVING Clauses

def test_simple_group_by():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='PUNCTUATION', value=','),
        Token(type='KEYWORD', value='COUNT'),
        Token(type='PUNCTUATION', value='('),
        Token(type='WILDCARD', value='*'),
        Token(type='PUNCTUATION', value=')'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1'),
        Token(type='KEYWORD', value='GROUP BY'),
        Token(type='IDENTIFIER', value='column1')
    ]
    parser = Parser(tokens)
    query = parser.parse()
    
    # Ensure the group_by_clause is a GroupByClause instance
    assert isinstance(query.group_by_clause, GroupByClause), f"Expected GroupByClause, got {type(query.group_by_clause)}"
    
    # Convert the GroupByClause to a dictionary to match the expected output
    group_by_dict = query.group_by_clause.to_dict()
    print(group_by_dict)
    
    # Perform assertions on the dictionary representation
    expected_group_by_dict = {
        'node_type': 'GroupByClause',
        'children': [{'node_type': 'Identifier', 'name': 'column1'}]
    }
    
    # Assert that the parsed GROUP BY clause matches the expected structure
    assert group_by_dict == expected_group_by_dict, f"Expected {expected_group_by_dict}, got {group_by_dict}"
    
    # Additional assertion on the specific column in the GROUP BY clause
    assert query.group_by_clause.children[0].name == 'column1'



def test_group_by_with_having():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='PUNCTUATION', value=','),
        Token(type='KEYWORD', value='COUNT'),
        Token(type='PUNCTUATION', value='('),
        Token(type='WILDCARD', value='*'),
        Token(type='PUNCTUATION', value=')'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1'),
        Token(type='KEYWORD', value='GROUP BY'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='KEYWORD', value='HAVING'),
        Token(type='KEYWORD', value='COUNT'),
        Token(type='PUNCTUATION', value='('),
        Token(type='WILDCARD', value='*'),
        Token(type='PUNCTUATION', value=')'),
        Token(type='OPERATOR', value='>'),
        Token(type='NUMBER', value='5')
    ]
    
    parser = Parser(tokens)
    query = parser.parse()
    
    # Convert the parsed query to a dictionary
    query_dict = query.to_dict()
    
    # Expected dictionary structure
    expected_dict = {
        'node_type': 'Query',
        'select_clause': {
            'node_type': 'SelectClause',
            'children': [
                {
                    'node_type': 'SelectItem',
                    'children': [{'node_type': 'Identifier', 'name': 'column1'}],
                    'expression': {'node_type': 'Identifier', 'name': 'column1'}
                },
                {
                    'node_type': 'SelectItem',
                    'children': [
                        {
                            'node_type': 'FunctionCall',
                            'name': 'COUNT',
                            'arguments': [{'node_type': 'Wildcard', 'value': '*'}]
                        }
                    ],
                    'expression': {
                        'node_type': 'FunctionCall',
                        'name': 'COUNT',
                        'arguments': [{'node_type': 'Wildcard', 'value': '*'}]
                    }
                }
            ]
        },
        'from_clause': {
            'node_type': 'FromClause',
            'table': {'node_type': 'Table', 'name': 'table1'}
        },
        'where_clause': None,
        'join_clauses': [],
        'group_by_clause': {
            'node_type': 'GroupByClause',
            'children': [{'node_type': 'Identifier', 'name': 'column1'}]
        },
        'having_clause': {
            'node_type': 'HavingClause',
            'condition': {
                'node_type': 'Comparison',
                'left': {
                    'node_type': 'FunctionCall',
                    'name': 'COUNT',
                    'arguments': [{'node_type': 'Literal', 'value': '*'}]
                },
                'operator': '>',
                'right': {'node_type': 'Literal', 'value': '5'}
            }
        },
        'order_by_clause': None
    }

    # Compare the parsed dictionary with the expected dictionary
    assert query_dict == expected_dict, (
        f"Expected: {expected_dict}, but got: {query_dict}"
    )

# 5. JOIN Clauses

def test_simple_inner_join():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='table1.column1'),
        Token(type='PUNCTUATION', value=','),
        Token(type='IDENTIFIER', value='table2.column2'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1'),
        Token(type='KEYWORD', value='INNER JOIN'),
        Token(type='IDENTIFIER', value='table2'),
        Token(type='KEYWORD', value='ON'),
        Token(type='IDENTIFIER', value='table1.id'),
        Token(type='OPERATOR', value='='),
        Token(type='IDENTIFIER', value='table2.id')
    ]
    parser = Parser(tokens)
    query = parser.parse()
    assert isinstance(query.join_clauses[0], JoinClause)
    assert query.join_clauses[0].table.name == 'table2'
    assert query.join_clauses[0].condition.left.name == 'table1.id'
    assert query.join_clauses[0].condition.right.name == 'table2.id'

def test_left_join():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='table1.column1'),
        Token(type='PUNCTUATION', value=','),
        Token(type='IDENTIFIER', value='table2.column2'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1'),
        Token(type='KEYWORD', value='LEFT JOIN'),
        Token(type='IDENTIFIER', value='table2'),
        Token(type='KEYWORD', value='ON'),
        Token(type='IDENTIFIER', value='table1.id'),
        Token(type='OPERATOR', value='='),
        Token(type='IDENTIFIER', value='table2.id')
    ]
    parser = Parser(tokens)
    query = parser.parse()
    assert isinstance(query.join_clauses[0], JoinClause)
    assert query.join_clauses[0].table.name == 'table2'
    assert query.join_clauses[0].condition.left.name == 'table1.id'
    assert query.join_clauses[0].condition.right.name == 'table2.id'

def test_multiple_joins():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='table1.column1'),
        Token(type='PUNCTUATION', value=','),
        Token(type='IDENTIFIER', value='table2.column2'),
        Token(type='PUNCTUATION', value=','),
        Token(type='IDENTIFIER', value='table3.column3'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1'),
        Token(type='KEYWORD', value='JOIN'),
        Token(type='IDENTIFIER', value='table2'),
        Token(type='KEYWORD', value='ON'),
        Token(type='IDENTIFIER', value='table1.id'),
        Token(type='OPERATOR', value='='),
        Token(type='IDENTIFIER', value='table2.id'),
        Token(type='KEYWORD', value='JOIN'),
        Token(type='IDENTIFIER', value='table3'),
        Token(type='KEYWORD', value='ON'),
        Token(type='IDENTIFIER', value='table2.id'),
        Token(type='OPERATOR', value='='),
        Token(type='IDENTIFIER', value='table3.id')
    ]
    parser = Parser(tokens)
    query = parser.parse()

    assert len(query.join_clauses) == 2



# 6. Aliased Columns and Tables

def test_aliased_columns():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='column1'),
        Token(type='KEYWORD', value='AS'),
        Token(type='IDENTIFIER', value='alias1'),
        Token(type='PUNCTUATION', value=','),
        Token(type='IDENTIFIER', value='column2'),
        Token(type='KEYWORD', value='AS'),
        Token(type='IDENTIFIER', value='alias2'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1')
    ]
    parser = Parser(tokens)
    query = parser.parse()
    assert query.select_clause.children[0].alias == 'alias1'
    assert query.select_clause.children[1].alias == 'alias2'

def test_aliased_tables():
    tokens = [
        Token(type='KEYWORD', value='SELECT'),
        Token(type='IDENTIFIER', value='t1.column1'),
        Token(type='PUNCTUATION', value=','),
        Token(type='IDENTIFIER', value='t2.column2'),
        Token(type='KEYWORD', value='FROM'),
        Token(type='IDENTIFIER', value='table1'),
        Token(type='IDENTIFIER', value='t1'),
        Token(type='PUNCTUATION', value=','),
        Token(type='IDENTIFIER', value='table2'),
        Token(type='IDENTIFIER', value='t2')
    ]
    parser = Parser(tokens)
    query = parser.parse()
    assert query.from_clause.table[0].name == 'table1'
    assert query.from_clause.table[0].alias == 't1'
