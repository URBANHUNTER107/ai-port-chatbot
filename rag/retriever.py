# import numpy as np
# from sentence_transformers import SentenceTransformer
# model = SentenceTransformer("all-MiniLM-L6-v2")

import numpy as np
from rag.embeddings import create_query_embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) *
        np.linalg.norm(b)
    )


def normalize_words(text):
    """
    Turns text into a clean set of lowercase words, with punctuation
    stripped out.
    """

    cleaned = "".join(
        ch if ch.isalnum() or ch.isspace() else " "
        for ch in text.lower()
    )

    return set(cleaned.split())


def strip_plural(word):
    """
    Very simple plural handling so "projects" (query) matches
    "project" (category) and vice versa.
    """

    if word.endswith("s") and len(word) > 3:
        return word[:-1]

    return word


def keyword_boost(query, chunk):
    """
    Bonus score when the query's words directly match the chunk's
    category or title. Helps specific chunks win over broad,
    generic-sounding chunks on pure semantic similarity.
    """

    query_words = {strip_plural(w) for w in normalize_words(query)}
    title_words = {strip_plural(w) for w in normalize_words(chunk["title"])}
    category_words = {strip_plural(w) for w in normalize_words(chunk["category"])}

    category_matches = query_words & category_words
    title_matches = query_words & title_words

    return (len(category_matches) * 0.30) + (len(title_matches) * 0.10)


# -----------------------------------------------------------------
# BROAD QUERY DETECTION
#
# Some questions aren't asking about ONE specific thing - they're
# asking for a full overview of Farhan ("tell me everything",
# "give me a summary", etc). For these, normal similarity-based
# retrieval isn't good enough, because it naturally favors whatever
# category scores highest and can end up ignoring entire sections
# (like education or projects) just because their wording didn't
# match as closely.
#
# So instead, if we detect one of these broad phrases in the query,
# we switch retrieval mode: guarantee at least one chunk from every
# category, instead of relying purely on similarity ranking.
# -----------------------------------------------------------------

BROAD_QUERY_PHRASES = [
    "tell me everything",
    "tell me all",
    "tell me about him",
    "tell me about farhan",
    "who is farhan",
    "give me an overview",
    "give me a summary",
    "full profile",
    "complete profile",
    "everything about him",
    "everything about farhan",
    "walk me through his profile",
    "introduce him",
    "introduce farhan",
]


def is_broad_query(query):
    """
    Checks if the query is asking for a full overview rather than
    something specific. Simple substring check against a known list
    of broad-question phrases.
    """

    query_lower = query.lower()

    return any(phrase in query_lower for phrase in BROAD_QUERY_PHRASES)


def get_best_chunk_per_category(query_embedding, chunks, embeddings):
    """
    For a broad "tell me everything" style question, this picks the
    single best-scoring chunk from EVERY category that exists in the
    data - so nothing gets left out just because it didn't score high
    enough on its own. This guarantees breadth (touch every section)
    instead of just depth (best matches overall, which can accidentally
    skip whole categories).
    """

    best_per_category = {}

    for i, embedding in enumerate(embeddings):

        chunk = chunks[i]
        category = chunk["category"]

        score = cosine_similarity(query_embedding, embedding)

        # if we haven't seen this category yet, or this chunk scores
        # higher than the one we currently have for this category,
        # keep this one instead
        if category not in best_per_category or score > best_per_category[category]["score"]:
            best_per_category[category] = {
                "score": float(score),
                "chunk": chunk
            }

    return list(best_per_category.values())


def retrieve(
    query,
    chunks,
    embeddings,
    top_k=20,
    min_score=0.20
):
    """
    Retrieve the most relevant chunks for a user query.

    - For normal, specific questions: uses semantic similarity +
      keyword boosting, same as before.

    - For broad "tell me everything" style questions: switches to
      guaranteeing one representative chunk from every category,
      so no section of the profile gets left out.
    """

    # query_embedding = model.encode(
    #     query,
    #     normalize_embeddings=True
    # )

    query_embedding = create_query_embedding(query)

    # ---- BROAD QUERY MODE ----
    if is_broad_query(query):

        results = get_best_chunk_per_category(
            query_embedding,
            chunks,
            embeddings
        )

        # still sort by score just for readability in debug prints
        results.sort(key=lambda x: x["score"], reverse=True)

        return results

    # ---- NORMAL QUERY MODE (unchanged from before) ----
    results = []

    for i, embedding in enumerate(embeddings):

        semantic_score = cosine_similarity(query_embedding, embedding)
        boost = keyword_boost(query, chunks[i])
        score = semantic_score + boost

        if score >= min_score:
            results.append({
                "score": float(score),
                "chunk": chunks[i]
            })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_k]