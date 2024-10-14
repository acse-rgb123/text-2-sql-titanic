import openai

def generate_sql_prompt(query, relevant_schema, relevant_gold_sql=None):
    """Generate SQL query using GPT-4 based on relevant schema and templates."""
    table_name = None
    relevant_cols = []
    
    # Parse relevant schema to get table and column names
    for col, _ in relevant_schema:
        if col and "Table" in col:
            table_name = col.split(",")[0].replace("Table", "").strip()
        if col and "Column" in col:
            relevant_cols.append(col.split(",")[1].replace("Column", "").strip())

    table_name = table_name or "titanic"
    sql_template = relevant_gold_sql[0][0] if relevant_gold_sql else None

    # Format the relevant columns into the query
    input_text = (
        f"Generate a valid SQL query for the question: {query}. "
        f"Use the table '{table_name}' and the relevant columns: {', '.join(relevant_cols)}. "
        f"Here is a template SQL query you can modify: {sql_template if sql_template else 'None'}."
        f"Dont include any comments, just the SQL code generated."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in SQL generation."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=150,
        temperature=0.5,
    )
    return response['choices'][0]['message']['content'].strip()


