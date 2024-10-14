import os
from modules.schema_extraction import extract_schema_from_db
from modules.vector_db_creation import create_vector_db_from_schema, create_vector_db_from_docs, create_vector_db_from_sql
from modules.data_retrieval import retrieve_relevant_data
from modules.sql_generation import generate_sql_prompt
from modules.sql_execution import execute_sql_query
from modules.result_interpretation import interpret_results
import openai

# imported openAI key
openai.api_key = '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'

# Define paths for data and metadata
TITANIC_DATA_FOLDER = 'titanic_data/'
METADATA_FOLDER = 'metadata/'

def run_pipeline(user_query):
    db_file = os.path.join(TITANIC_DATA_FOLDER, 'titanic.db')
    docs_file = os.path.join(TITANIC_DATA_FOLDER, 'titanic_documentation.txt')
    gold_sql_file = os.path.join(TITANIC_DATA_FOLDER, 'titanic_gold_sql_queries.txt')

    # Step 1: Extract schema from the database
    schema = extract_schema_from_db(db_file)

    # Step 2: Vectorize data if vector databases don't exist
    if not os.path.exists(os.path.join(METADATA_FOLDER, "schema_index.faiss")):
        create_vector_db_from_schema(schema, metadata_folder=METADATA_FOLDER)
    if not os.path.exists(os.path.join(METADATA_FOLDER, "documentation_index.faiss")):
        with open(docs_file, 'r') as f:
            docs = f.readlines()
        create_vector_db_from_docs(docs, metadata_folder=METADATA_FOLDER)
    if not os.path.exists(os.path.join(METADATA_FOLDER, "gold_sql_index.faiss")):
        with open(gold_sql_file, 'r') as f:
            gold_sql_queries = f.readlines()
        create_vector_db_from_sql(gold_sql_queries, metadata_folder=METADATA_FOLDER)

    # Step 3: Retrieve relevant data
    relevant_schema = retrieve_relevant_data(user_query, db_type="schema", metadata_folder=METADATA_FOLDER)
    relevant_gold_sql = retrieve_relevant_data(user_query, db_type="gold_sql", metadata_folder=METADATA_FOLDER)

    # Step 4: Generate SQL query
    sql_query = generate_sql_prompt(user_query, relevant_schema, relevant_gold_sql)

    # Step 5: Execute SQL query
    results = execute_sql_query(db_file, sql_query)

    # Step 6: Interpret results
    interpretation = interpret_results(results, user_query)

    print(f"Generated SQL Query:\n{sql_query}")
    print(f"Query Results:\n{results}")
    print(f"Interpretation:\n{interpretation}")

if __name__ == "__main__":
    user_query = input("Enter your query: ")
    run_pipeline(user_query)
