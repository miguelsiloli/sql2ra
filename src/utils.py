from .ast.derived_types import FunctionCall, Identifier


def convert_to_query(query):
    # Ensure the query has a select clause
    select_clause = query.select_clause
    if not select_clause:
        return ""

    # Start building the SELECT part of the SQL query
    select_parts = []

    for item in select_clause.children:
        expression = item.expression
        alias = item.alias

        if isinstance(expression, FunctionCall):
            function_name = expression.name
            arguments = expression.arguments
            arg_str = ", ".join([arg.name for arg in arguments if isinstance(arg, Identifier)])
            expression_str = f"{function_name}({arg_str})"
        elif isinstance(expression, Identifier):
            expression_str = expression.name

        if alias:
            select_parts.append(f"{expression_str} AS {alias}")
        else:
            select_parts.append(expression_str)

    # Join the select parts into a canonical SELECT clause
    select_clause_str = "SELECT " + ", ".join(select_parts)

    # Handle the FROM clause
    from_clause = query.from_clause
    table = from_clause.table
    table_name = table[0].name
    from_clause_str = f"FROM {table_name}"

    # Combine the SELECT and FROM clauses
    canonical_query = f"{select_clause_str} {from_clause_str}"

    return canonical_query


def convert_to_canonical(query):
    # Initialize a list to hold the logical expressions
    logical_expressions = []

    # Extract the select clause
    select_clause = query.select_clause
    if not select_clause:
        return logical_expressions

    # Process each SelectItem in the select clause
    for item in select_clause.children:
        expression = item.expression
        alias = item.alias

        if isinstance(expression, FunctionCall):
            function_name = expression.name
            arguments = [arg.name for arg in expression.arguments if isinstance(arg, Identifier)]
            logical_expressions.append(
                {
                    "type": "function_call",
                    "function": function_name,
                    "arguments": arguments,
                    "alias": alias,
                }
            )
        elif isinstance(expression, Identifier):
            logical_expressions.append(
                {"type": "identifier", "name": expression.name, "alias": alias}
            )

    # Process the from clause
    from_clause = query.from_clause
    table = from_clause.table
    logical_expressions.append({"type": "table", "name": table[0].name})

    return logical_expressions
