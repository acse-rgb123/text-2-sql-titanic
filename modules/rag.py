import openai
import faiss
import numpy as np
import os

class RAG:
    """
    Class to handle Retrieval-Augmented Generation for retrieving relevant data.
    """

    def __init__(self, query, vector_db_type="schema", metadata_folder="metadata", top_n=10):
        self.query = query
        self.vector_db_type = vector_db_type
        self.metadata_folder = metadata_folder
        self.top_n = top_n

    def retrieve_relevant_data(self):
        """
        Retrieves relevant data from the vector database based on the query.
        """
        index_file = os.path.join(self.metadata_folder, f"{self.vector_db_type}_index.faiss")
        if not os.path.exists(index_file):
            print(f"{self.vector_db_type} index file is missing. Ensure vectorization is done first.")
            return []

        index = faiss.read_index(index_file)
        query_embedding = openai.Embedding.create(input=self.query, model="text-embedding-ada-002")['data'][0]['embedding']
        query_embedding = np.array(query_embedding).astype('float32').reshape(1, -1)

        D, I = index.search(query_embedding, self.top_n)
        return [(I[0][idx], D[0][idx]) for idx in range(self.top_n)]
