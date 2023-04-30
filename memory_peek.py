import chromadb

from chromadb.config import Settings
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=".db"))
collection = client.get_or_create_collection(name="previous_conversations")

print(collection.peek()['documents'])
# ['The Color of Magic', 'Wyrd Sisters', 'Guards! Guards!', 'Red Mars', 'Blue Mars', 'The Iliad', 'The Odyssey']
