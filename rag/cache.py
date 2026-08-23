import hashlib
import pickle
from pathlib import Path

# where we'll store the saved (cached) embeddings
CACHE_FILE = Path(__file__).parent.parent / "data" / "embeddings_cache.pkl"


def get_file_hash(filepath):
    """
    Creates a short fingerprint of a file's contents.
    If the file changes even slightly, this fingerprint changes too -
    that's how we know when personal_data.json has been edited.
    """
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def load_cached_embeddings(source_json_path):
    """
    Tries to load previously saved chunks + embeddings.
    Returns None if there's no valid cache (first run, or file was edited).
    """

    if not CACHE_FILE.exists():
        print(f"CACHE DEBUG: cache file does not exist at {CACHE_FILE}")
        return None

    current_hash = get_file_hash(source_json_path)

    with open(CACHE_FILE, "rb") as f:
        cached = pickle.load(f)

    # if the JSON file has changed since we last cached, the cache is stale
    if cached["source_hash"] != current_hash:
        print(f"CACHE DEBUG: hash mismatch. cached={cached['source_hash']} current={current_hash}")
        return None

    print("CACHE DEBUG: cache hit, using cached embeddings")
    return cached["chunks"], cached["embeddings"]


def save_embeddings_to_cache(source_json_path, chunks, embeddings):
    """
    Saves chunks + embeddings + a fingerprint of the source JSON,
    so next time we can skip recomputing everything.
    """

    current_hash = get_file_hash(source_json_path)

    with open(CACHE_FILE, "wb") as f:
        pickle.dump({
            "source_hash": current_hash,
            "chunks": chunks,
            "embeddings": embeddings
        }, f)