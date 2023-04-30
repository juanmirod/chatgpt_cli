import uuid
import chromadb

from chromadb.config import Settings
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=".db"))
collection = client.get_or_create_collection(name="previous_conversations")


def save_interchange(user_prompt, assistant_response):
    unique_id = uuid.uuid4()
    collection.add(
        documents=[f'user: {user_prompt}\nyou: {assistant_response}'],
        ids=[f'{unique_id}']  # ids must be unique
    )


def get_related(search_term):
    return collection.query(query_texts=[search_term], n_results=2)
