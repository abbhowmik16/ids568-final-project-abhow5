"""
Formal Retrieval Evaluation for RAG System
Addresses Milestone 6 feedback by adding precision@k and recall@k.
"""

import json
from pathlib import Path

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from rag_pipeline import (
    DATA_DIR,
    load_documents,
    create_chunks,
    build_embeddings,
    build_faiss_index,
    retrieve,
)


EVAL_QUERIES = [
    {
        "query": "What is RAG and how does it work?",
        "relevant_sources": ["rag_basics.txt"],
    },
    {
        "query": "Why is chunking important in a RAG pipeline?",
        "relevant_sources": ["chunking.txt"],
    },
    {
        "query": "How do embeddings help retrieval?",
        "relevant_sources": ["embeddings.txt"],
    },
    {
        "query": "What is the role of a vector database?",
        "relevant_sources": ["vector_databases.txt"],
    },
    {
        "query": "What does grounding mean in RAG?",
        "relevant_sources": ["grounding_evaluation.txt"],
    },
]


def precision_at_k(retrieved_sources, relevant_sources, k):
    retrieved_k = retrieved_sources[:k]
    relevant_set = set(relevant_sources)

    relevant_count = sum(
        1 for source in retrieved_k if source in relevant_set
    )

    return relevant_count / k


def recall_at_k(retrieved_sources, relevant_sources, k):
    retrieved_k = set(retrieved_sources[:k])
    relevant_set = set(relevant_sources)

    matched_relevant = retrieved_k.intersection(relevant_set)

    return len(matched_relevant) / len(relevant_set)


def main():
    print("=" * 60)
    print("FORMAL RAG RETRIEVAL EVALUATION")
    print("=" * 60)

    documents = load_documents(DATA_DIR)
    chunks = create_chunks(documents)
    model, embeddings = build_embeddings(chunks)
    index = build_faiss_index(embeddings)

    results = []

    for item in EVAL_QUERIES:
        query = item["query"]
        relevant_sources = item["relevant_sources"]

        retrieved_chunks, retrieval_ms = retrieve(query, model, index, chunks, k=3)
        retrieved_sources = [chunk["source"] for chunk in retrieved_chunks]

        p_at_1 = precision_at_k(retrieved_sources, relevant_sources, 1)
        p_at_3 = precision_at_k(retrieved_sources, relevant_sources, 3)
        r_at_3 = recall_at_k(retrieved_sources, relevant_sources, 3)

        result = {
            "query": query,
            "relevant_sources": relevant_sources,
            "retrieved_sources": retrieved_sources,
            "precision_at_1": round(p_at_1, 3),
            "precision_at_3": round(p_at_3, 3),
            "recall_at_3": round(r_at_3, 3),
            "retrieval_ms": round(retrieval_ms, 2),
        }

        results.append(result)

        print(f"\nQuery: {query}")
        print(f"Relevant: {relevant_sources}")
        print(f"Retrieved: {retrieved_sources}")
        print(f"Precision@1: {p_at_1:.3f}")
        print(f"Precision@3: {p_at_3:.3f}")
        print(f"Recall@3: {r_at_3:.3f}")
        print(f"Retrieval ms: {retrieval_ms:.2f}")

    avg_p1 = sum(r["precision_at_1"] for r in results) / len(results)
    avg_p3 = sum(r["precision_at_3"] for r in results) / len(results)
    avg_r3 = sum(r["recall_at_3"] for r in results) / len(results)

    summary = {
        "average_precision_at_1": round(avg_p1, 3),
        "average_precision_at_3": round(avg_p3, 3),
        "average_recall_at_3": round(avg_r3, 3),
        "num_queries": len(results),
    }

    output = {
        "summary": summary,
        "results": results,
    }

    Path("logs").mkdir(exist_ok=True)
    output_path = Path("logs/retrieval_metrics.json")
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(json.dumps(summary, indent=2))
    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()