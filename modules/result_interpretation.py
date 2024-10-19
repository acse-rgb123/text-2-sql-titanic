class ResultInterpretation:
    """
    Class to handle interpretation of SQL results using the LLM.
    """

    def __init__(self, llm):
        self.llm = llm

    def interpret_results(self, results, user_query):
        """
        Interprets results using the LLM.
        """
        return self.llm.interpret_results(results, user_query)

    def display_results(self, results, user_query):
        """
        Displays the interpreted results using the LLM.
        """
        interpretation = self.interpret_results(results, user_query)
        print(f"Interpretation of results for query '{user_query}':\n{interpretation}")
