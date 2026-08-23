import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("gemini_api")

if not api_key:
    raise ValueError("Gemini API key not found")

client = genai.Client(api_key=api_key)

MODEL = "gemini-embedding-001"


def create_embeddings(chunks):

    texts = []

    for chunk in chunks:

        text = f"""
Category: {chunk['category']}

Title: {chunk['title']}

{chunk['text']}
"""

        texts.append(text)

    response = client.models.embed_content(
        model=MODEL,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=768
        )
    )

    return [embedding.values for embedding in response.embeddings]

def create_query_embedding(query):

    response = client.models.embed_content(
        model=MODEL,
        contents=query,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=768
        )
    )

    return response.embeddings[0].values





#Old Code
'''
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):

    texts = []

    for chunk in chunks:

        text = f"""
Category: {chunk['category']}

Title: {chunk['title']}

{chunk['text']}
"""

        texts.append(text)

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings
'''