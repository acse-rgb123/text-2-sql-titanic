import os
import openai
import json
from modules import (
    extract_schema_from_db,
    create_vector_db_from_schema, create_vector_db_from_docs, create_vector_db_from_sql,
    retrieve_relevant_data,
    generate_sql_prompt,
    execute_sql_query,
    interpret_results
)
# imported openAI key
openai.api_key = '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'

def run_pipeline(config_file, user_query=None):
    """
    Run the query pipeline with dynamic paths and settings loaded from a JSON configuration file.

    :param config_file: Path to the JSON configuration file containing paths and settings.
    :param user_query: Optional user query. If None, the query from the JSON file is used.
    """
    
    # Load the paths and user query from the JSON configuration file
    with open(config_file, 'r') as f:
        config = json.load(f)

    db_file = config["db_file"]
    docs_file = config["docs_file"]
    gold_sql_file = config["gold_sql_file"]
    metadata_folder = config["metadata_folder"]

    # Use the query provided in the function if available, otherwise use the one in the JSON config
    if user_query is None:
        user_query = config["user_query"]

    # Step 1: Extract schema from the database
    schema = extract_schema_from_db(db_file)

    # Step 2: Vectorize data if vector databases don't exist
    if not os.path.exists(os.path.join(metadata_folder, "schema_index.faiss")):
        create_vector_db_from_schema(schema, metadata_folder=metadata_folder)
    if not os.path.exists(os.path.join(metadata_folder, "documentation_index.faiss")):
        with open(docs_file, 'r') as f:
            docs = f.readlines()
        create_vector_db_from_docs(docs, metadata_folder=metadata_folder)
    if not os.path.exists(os.path.join(metadata_folder, "gold_sql_index.faiss")):
        with open(gold_sql_file, 'r') as f:
            gold_sql_queries = f.readlines()
        create_vector_db_from_sql(gold_sql_queries, metadata_folder=metadata_folder)

    # Step 3: Retrieve relevant schema and gold SQL data
    relevant_schema = retrieve_relevant_data(user_query, db_type="schema", metadata_folder=metadata_folder)
    relevant_gold_sql = retrieve_relevant_data(user_query, db_type="gold_sql", metadata_folder=metadata_folder)

    # Step 4: Generate SQL query using GPT-4
    sql_query = generate_sql_prompt(user_query, schema, relevant_gold_sql)

    # Step 5: Execute the generated SQL query
    results = execute_sql_query(db_file, sql_query)

    # Step 6: Interpret the results
    interpretation = interpret_results(results, user_query)

    # Print the SQL query, results, and interpretation
    print(f"Generated SQL Query:\n{sql_query}")
    print(f"Query Results:\n{results}")
    print(f"Interpretation:\n{interpretation}")

if __name__ == "__main__":
    # Use the JSON configuration file to provide paths and settings
    config_file = 'config.json'  # Specify the path to the JSON file
    
    # Ask the user for a query or hit enter to use the JSON query
    user_input = input("Enter your query (or press Enter to use the query from the JSON file): ")
    
    if user_input.strip():
        # If the user provided input, use that as the query
        run_pipeline(config_file, user_query=user_input)
    else:
        # If no input was provided, use the query from the JSON file
        run_pipeline(config_file)