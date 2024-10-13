import openai
import faiss
import numpy as np
import os

def create_vector_db(data, db_type, metadata_folder):
    """Create a vector database using FAISS."""
    embeddings = []
    descriptions = []

    for item in data:
        description = str(item)
        descriptions.append(description)
        embedding = openai.Embedding.create(input=description, model="text-embedding-ada-002")['data'][0]['embedding']
        embeddings.append(embedding)

    embeddings = np.array(embeddings).astype('float32')
    d = embeddings.shape[1]

    if db_type == "schema":
        index = faiss.IndexFlatIP(d)  # Flat index for schema
    elif db_type == "documentation":
        nlist = 100  # Number of clusters
        quantizer = faiss.IndexFlatIP(d)
        index = faiss.IndexIVFFlat(quantizer, d, nlist)
        index.train(embeddings)
    elif db_type == "gold_sql":
        index = faiss.IndexHNSWFlat(d, 32)

    index.add(embeddings)

    # Save index and descriptions
    faiss.write_index(index, os.path.join(metadata_folder, f"{db_type}_index.faiss"))
    if db_type != "schema":
        np.save(os.path.join(metadata_folder, f"{db_type}_descriptions.npy"), descriptions)

    return index


def create_vector_db_from_schema(schema, metadata_folder):
    """Vectorize schema metadata."""
    column_descriptions = [f"Table {table}, Column {col}, Type {col_type}"
                           for table, cols in schema.items()
                           for col, col_type in cols.items()]
    return create_vector_db(column_descriptions, db_type="schema", metadata_folder=metadata_folder)


def create_vector_db_from_docs(docs, metadata_folder):
    """Vectorize documentation data."""
    return create_vector_db(docs, db_type="documentation", metadata_folder=metadata_folder)


def create_vector_db_from_sql(queries, metadata_folder):
    """Vectorize gold SQL queries."""
    return create_vector_db(queries, db_type="gold_sql", metadata_folder=metadata_folder)
