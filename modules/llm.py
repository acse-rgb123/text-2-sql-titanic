import openai

class LLM:
    """
    Class to handle interactions with GPT-4 for various tasks.
    """

    def __init__(self, model="gpt-4"):
        self.model = model

    def generate_sql(self, user_query, schema, relevant_gold_sql):
        """
        Uses GPT-4 to generate an SQL query based on the user query, schema, and relevant SQL.
        """
        prompt = f"""
        Generate an SQL query based on the following:
        User query: {user_query}
        Schema: {schema}
        Relevant gold SQL: {relevant_gold_sql}
        """
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            max_tokens=150
        )
        return response['choices'][0]['text'].strip()

    def interpret_results(self, results, user_query):
        """
        Uses GPT-4 to interpret and provide a natural language explanation of the SQL results.
        """
        formatted_results = "\n".join([str(row) for row in results])
        
        prompt = f"""
        The following are the results of an SQL query:
        Results: {formatted_results}
        
        User query: {user_query}
        
        Please provide a detailed natural language interpretation of these results.
        """
        
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            max_tokens=200
        )
        return response['choices'][0]['text'].strip()

    def augment_query(self, user_query):
        """
        Uses GPT-4 to augment the user query with additional context or data.
        """
        prompt = f"""
        Augment the following user query with additional context:
        User query: {user_query}
        """
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            max_tokens=100
        )
        return response['choices'][0]['text'].strip()
