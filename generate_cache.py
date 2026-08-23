# One-time local script to build the embeddings cache file.
# Run this manually whenever personal_data.json changes.
# Not used by the deployed app - back.py just reads the file this creates.

from pathlib import Path

from rag.loader import load_personal_data
from rag.chunker import create_chunks
from rag.embeddings import create_embeddings
from rag.cache import save_embeddings_to_cache

json_path = Path(__file__).parent / "data" / "personal_data.json"

data = load_personal_data()
chunks = create_chunks(data)
embeddings = create_embeddings(chunks)

save_embeddings_to_cache(json_path, chunks, embeddings)

print("Cache rebuilt successfully.")