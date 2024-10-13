import faiss
import numpy as np
import openai
import os

def retrieve_relevant_data(query, db_type="schema", metadata_folder="metadata", top_n=10):
    """Retrieve top-N most relevant data from the vector database."""
    index_file = os.path.join(metadata_folder, f"{db_type}_index.faiss")
    desc_file = os.path.join(metadata_folder, f"{db_type}_descriptions.npy") if db_type != "schema" else None

    # Check if the FAISS index exists
    if not os.path.exists(index_file):
        print(f"{db_type} index file is missing. Ensure vectorization is done first.")
        return []

    index = faiss.read_index(index_file)

    descriptions = None
    if db_type != "schema" and os.path.exists(desc_file):
        descriptions = np.load(desc_file, allow_pickle=True)

    query_embedding = openai.Embedding.create(input=query, model="text-embedding-ada-002")['data'][0]['embedding']
    query_embedding = np.array(query_embedding).astype('float32').reshape(1, -1)

    D, I = index.search(query_embedding, top_n)

    if db_type == "schema":
        return [(index_file, D[0][idx]) for idx in range(top_n)]
    else:
        return [(descriptions[i], D[0][idx]) for idx, i in enumerate(I[0][:top_n])]

