import openai
import os

# Import everything from the 'modules' package
from modules import UserInput, Vectorizing, RAG, SQLGenerationAndExecution, ResultInterpretation, LLM

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def run_pipeline(config_file, user_query=None):
    # Step 1: Retrieve data from configuration file
    user_input = UserInput(None, config_file)  # Pass None for input_data if not needed
    config_data = user_input.retrieve_data()

    # Check if the user provided a query, otherwise fall back to the config file
    if not user_query:
        user_query = config_data.get('user_query')  # Use query from config file if no user query is provided

    # Step 2: Vectorize schema
    schema = config_data['schema']  # Assuming the schema is provided in the config
    vectorizer = Vectorizing()
    vectorizer.create_vector_db_from_schema(schema)

    # Step 3: Retrieve relevant schema and gold SQL data
    rag = RAG()
    relevant_schema = rag.retrieve_relevant_data(user_query, db_type="schema")
    relevant_gold_sql = rag.retrieve_relevant_data(user_query, db_type="gold_sql")

    # Step 4: Instantiate LLM and generate SQL query
    llm = LLM()
    sql_gen_exec = SQLGenerationAndExecution(llm)
    sql_query = sql_gen_exec.generate_sql(user_query, schema, relevant_gold_sql)

    # Step 5: Execute the SQL query
    db_file = config_data['db_file']
    results = sql_gen_exec.execute_sql_query(db_file, sql_query)

    # Step 6: Interpret and display the results using GPT
    result_interpreter = ResultInterpretation(llm)
    result_interpreter.display_results(results, user_query)

if __name__ == "__main__":
    config_file = "config.json"  # Path to the JSON config file
    
    # Allow the user to input their own query
    user_query = input("Enter your query (or press Enter to use the query from config file): ").strip()
    
    # Pass user_query as None if the user presses Enter
    if user_query == "":
        user_query = None
    
    run_pipeline(config_file, user_query)
