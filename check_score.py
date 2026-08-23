# This is a throwaway script - just for figuring out a good min_score
# and checking that retrieval + keyword boosting are working right.

from rag.loader import load_personal_data
from rag.chunker import create_chunks
from rag.embeddings import create_embeddings
from rag.retriever import retrieve

# A mix of questions that SHOULD match something,
# and questions that SHOULD NOT match anything.
test_queries = [
    "What projects has Farhan built?",
    "Tell me about his internship",
    "What is his favorite pizza topping?",
    "Does he know how to skydive?",
]

data = load_personal_data()
chunks = create_chunks(data)
embeddings = create_embeddings(chunks)

for query in test_queries:

    print("\n" + "=" * 70)
    print("QUERY:", query)
    print("=" * 70)

    # min_score=0 here so we can see the FULL ranked list, unfiltered
    results = retrieve(query, chunks, embeddings, top_k=8, min_score=0)

    for result in results:
        print(f"{result['score']:.3f}   {result['chunk']['title']}")