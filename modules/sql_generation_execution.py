class SQLGenerationAndExecution:
    """
    Class to handle SQL generation and execution.
    """

    def __init__(self, llm):
        self.llm = llm

    def generate_sql(self, user_query, schema, relevant_gold_sql):
        """
        Generates SQL using the LLM.
        """
        return self.llm.generate_sql(user_query, schema, relevant_gold_sql)

    def execute_sql_query(self, db_file, sql_query):
        """
        Executes the SQL query.
        """
        import sqlite3
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()
        return results
