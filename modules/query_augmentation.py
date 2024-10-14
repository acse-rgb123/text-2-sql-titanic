from modules.data_retrieval import retrieve_relevant_data
import openai

def extract_conditions_from_query(user_query, columns):
    """
    Extract conditions from the user query based on the schema columns.
    """
    # Use GPT-4 or other models to extract conditions from the query.
    input_text = (
        f"Extract the WHERE and JOIN conditions if there are any from the following query: '{user_query}'. "
        f"Use the available columns: {', '.join(columns)}."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in this schema and SQL generation."},
            {"role": "user", "content": input_text}
        ],
        max_tokens=100,
        temperature=0.5,
    )

    extracted_conditions = response['choices'][0]['message']['content'].strip()
    
    return extracted_conditions

def augment_sql_using_llm(previous_sql, user_query, relevant_gold_sql=None):
    """
    Use an LLM to augment the previous SQL query based on the user's query.
    """
    # Prepare the input text for GPT-4
    prompt = (
        f"You are an SQL expert. The following is a gold standard SQL query:\n"
        f"{previous_sql}\n\n"
        f"Now, modify the SQL query to answer this user question: '{user_query}'."
        f" You can use the existing structure but ensure the new SQL query answers the user's question correctly."
    )

    # Send the prompt to GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an SQL expert."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.5,
    )

    # Get the augmented SQL from GPT-4's response
    augmented_sql = response['choices'][0]['message']['content'].strip()

    # Clean up any unnecessary backticks or formatting
    if augmented_sql.startswith('```') and augmented_sql.endswith('```'):
        augmented_sql = augmented_sql.strip('```').strip()

    return augmented_sql

def handle_query_augmentation(user_query, vector_db, columns):
    """
    Check if a similar query has been asked before, and augment the SQL if found.
    """
    similar_query_data = retrieve_relevant_data(user_query, db_type="gold_sql", metadata_folder="metadata", top_n=1)
    if similar_query_data:
        previous_sql = similar_query_data[0][0]  # Assuming first element is the SQL query
        print(f"Found a similar query: {previous_sql}")
        return augment_sql_using_llm(previous_sql, user_query, columns)
    return None
