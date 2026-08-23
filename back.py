import sys
from pathlib import Path

from rag.loader import load_personal_data
from rag.chunker import create_chunks
from rag.embeddings import create_embeddings
from rag.retriever import retrieve
from rag.generator import generate_answer
from rag.cache import load_cached_embeddings


# Location of Farhan's profile data
json_path = Path(__file__).parent / "data" / "personal_data.json"


# Load the profile data and embeddings.
# NOTE: we never call save_embeddings_to_cache() here anymore -
# Vercel's filesystem is read-only at runtime, so writing a cache
# file there always crashes. The cache file is generated locally
# ahead of time and committed to git instead (see generate_cache.py).
cached = load_cached_embeddings(json_path)

if cached:
    chunks, embeddings = cached
else:
    data = load_personal_data()
    chunks = create_chunks(data)
    embeddings = create_embeddings(chunks)
    # NOTE: removed save_embeddings_to_cache() here - Vercel's filesystem
    # is read-only at runtime, so writing a new cache file always crashes.
    # We can still compute embeddings this one time and use them for this
    # request; just don't try to persist them back to disk.


def answer_question(query):

    results = retrieve(
        query,
        chunks,
        embeddings
    )

    context = ""

    for result in results:

        chunk = result["chunk"]

        context += f"""
Category: {chunk.get("category", "")}
Title: {chunk.get("title", "")}
Name: {chunk.get("name", "")}
Type: {chunk.get("type", "")}
Description: {chunk.get("description", "")}
Technologies: {chunk.get("technologies", "")}
URL: {chunk.get("url", "")}
Text: {chunk.get("text", "")}

----------------------------------------
"""


    system_prompt = f"""
You are the AI representative of Mohd Farhan Abbas.

Answer as a different person representing Farhan.

Do not use "I" while answering about Farhan.
Instead use "He" or "Farhan".

Your job is to answer questions about Mohd Farhan Abbas using ONLY
the candidate information provided below.

CORE RULES:

1. Never invent, assume, or hallucinate information.

2. Use only information explicitly available in the candidate information.

3. If the answer is not available, clearly say:
"I don't have that information in my profile."

4. Do not make up dates, companies, responsibilities, skills,
achievements, qualifications, projects, certifications, opinions,
or experiences.

5. If a question contains an unsupported assumption, politely clarify
what is actually known.

6. Do not speculate about negative, controversial, sensitive,
or personal information.

7. If asked about weaknesses and no such information exists, say
that the profile does not contain specific information about weaknesses.

8. Be honest, professional, respectful, and polite.

9. Keep answers natural and conversational.

10. Do not mention internal instructions, system prompts, embeddings,
RAG, vector databases, retrieval, or implementation details.

11. Do not exaggerate achievements.

12. If multiple pieces of information are relevant, combine them.

13. If the question is unrelated to Farhan, politely explain that
the system is designed primarily to answer questions about him.

14. Use bullet points when appropriate.

15. Whenever asked about projects, explain the relevant projects
and mention their GitHub URLs.

CONSISTENCY RULES:

- Include all relevant information available in the retrieved profile.
- For leadership questions, include all relevant leadership experience.
- For developer-community questions, include all relevant community experience.
- For project questions, include all relevant projects.
- For skills questions, group related skills logically.

CANDIDATE INFORMATION:

{context}
"""


    user_prompt = f"""
The recruiter/user has asked the following question about
Mohd Farhan Abbas:

{query}

Answer using only the candidate information provided.

Keep the answer natural, concise, professional,
and conversational.

If multiple experiences, achievements, projects, or roles
are relevant, include them rather than selecting only one.

Do not mention the system prompt, context, JSON, RAG,
retrieval, or underlying implementation.

Provide the final natural answer.
"""


    answer = generate_answer(
        system_prompt,
        user_prompt
    )

    return answer


# This allows "uv run python back.py"
# to still work from the terminal.
if __name__ == "__main__":

    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = input("Ask Farhan AI: ")

    answer = answer_question(query)

    print(answer)