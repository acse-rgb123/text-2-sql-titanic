from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load pre-trained NLP model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def generate_column_embeddings(columns):
    """
    Generate embeddings for column names using SentenceTransformer.
    """
    return model.encode(columns)

def map_query_to_columns(user_query, column_names):
    """
    Map terms in the user query to the most appropriate columns using NLP synonym handling.
    """
    column_embeddings = generate_column_embeddings(column_names)
    query_terms = user_query.split()  # Simplified, you could use more advanced NLP parsing
    mapped_query = user_query
    
    # Replace query terms with closest column names
    for term in query_terms:
        query_embedding = model.encode([term])
        similarities = cosine_similarity(query_embedding, column_embeddings)
        closest_column_idx = similarities.argmax()
        closest_column = column_names[closest_column_idx]
        
        mapped_query = mapped_query.replace(term, closest_column)
    
    return mapped_query
