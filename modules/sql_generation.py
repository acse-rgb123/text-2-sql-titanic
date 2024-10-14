import openai

def generate_sql_prompt(query, schema, relevant_gold_sql=None):
    """Generate SQL query using GPT-4 based on relevant schema and templates."""
    
    table_name = None
    relevant_cols = []
    
    # Ensure the schema is a valid dictionary or list of tuples and extract table and column names
    if isinstance(schema, dict):
        # Handle case where schema is a dictionary
        table_name = list(schema.keys())[0]  # Assuming first table is the target
        relevant_cols = list(schema[table_name].keys())
    elif isinstance(schema, list):
        # Handle case where schema is a list of tuples
        for col in schema:
            if isinstance(col, tuple) and len(col) >= 2:
                if "Table" in col[0]:
                    table_name = col[0].replace("Table", "").strip()
                if "Column" in col[0]:
                    relevant_cols.append(col[1].strip())

    # If no valid schema or columns are found, return an error
    if not table_name or not relevant_cols:
        return "Error: No valid schema or columns found. SQL query cannot be generated."

    # Use the first relevant gold SQL query if available; otherwise, return an error
    if relevant_gold_sql:
        sql_template = relevant_gold_sql[0][0]  # Get the first gold SQL query template
    else:
        return "Error: No relevant gold SQL template found to modify for this query."

    # Prepare the prompt for GPT-4
    input_text = (
        f"Modify the following SQL query based on the user question: '{query}'. "
        f"Use the table '{table_name}' and the columns: {', '.join(relevant_cols)}. "
        f"Here is the SQL query to modify: {sql_template}."
        f"Only return the modified SQL query."
    )

    # Call GPT-4 API to modify the SQL query
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in SQL generation and modifying SQL queries based on context."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=150,
        temperature=0.5,
    )
    
    # Return the modified SQL query, ensuring no unnecessary characters
    return response['choices'][0]['message']['content'].strip()




