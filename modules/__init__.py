# modules/__init__.py

# Import necessary functions from each module and expose them

# From schema_extraction.py
from .schema_extraction import extract_schema_from_db

# From vector_db_creation.py
from .vector_db_creation import create_vector_db_from_schema, create_vector_db_from_docs, create_vector_db_from_sql

# From data_retrieval.py
from .data_retrieval import retrieve_relevant_data

# From sql_generation.py
from .sql_generation import generate_sql_prompt

# From sql_execution.py
from .sql_execution import execute_sql_query

# From result_interpretation.py
from .result_interpretation import interpret_results

# Now all of these functions are exposed when you do a block import from 'modules'
