"""
Chunk Size Comparison for RAG System
Addresses Milestone 6 feedback by comparing retrieval performance across chunk sizes.
"""

import json
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from rag_pipeline import DATA_DIR, load_documents, EMBEDDING_MODEL_NAME


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


def chunk_text_custom(text, chunk_size, chunk_overlap):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - chunk_overlap

    return chunks


def create_chunks_custom(documents, chunk_size, chunk_overlap):
    all_chunks = []

    for doc in documents:
        doc_chunks = chunk_text_custom(doc["text"], chunk_size, chunk_overlap)

        for i, chunk in enumerate(doc_chunks):
            all_chunks.append(
                {
                    "source": doc["source"],
                    "chunk_id": i,
                    "content": chunk,
                }
            )

    return all_chunks


def build_index(chunks, model):
    texts = [chunk["content"] for chunk in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index, embeddings


def retrieve_custom(query, model, index, chunks, k=3):
    start = time.time()

    query_embedding = model.encode([query], convert_to_numpy=True).astype("float32")
    distances, indices = index.search(query_embedding, k)

    retrieval_ms = (time.time() - start) * 1000

    retrieved = []
    for rank, idx in enumerate(indices[0], start=1):
        retrieved.append(
            {
                "rank": rank,
                "source": chunks[idx]["source"],
                "chunk_id": chunks[idx]["chunk_id"],
                "distance": float(distances[0][rank - 1]),
            }
        )

    return retrieved, retrieval_ms


def precision_at_k(retrieved_sources, relevant_sources, k):
    retrieved_k = retrieved_sources[:k]
    relevant_set = set(relevant_sources)
    relevant_count = sum(1 for source in retrieved_k if source in relevant_set)
    return relevant_count / k


def recall_at_k(retrieved_sources, relevant_sources, k):
    retrieved_k = set(retrieved_sources[:k])
    relevant_set = set(relevant_sources)
    return len(retrieved_k.intersection(relevant_set)) / len(relevant_set)


def main():
    print("=" * 60)
    print("CHUNK SIZE COMPARISON")
    print("=" * 60)

    documents = load_documents(DATA_DIR)
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    configs = [
        {"chunk_size": 300, "chunk_overlap": 30},
        {"chunk_size": 500, "chunk_overlap": 50},
        {"chunk_size": 800, "chunk_overlap": 80},
    ]

    all_results = []

    for config in configs:
        chunk_size = config["chunk_size"]
        chunk_overlap = config["chunk_overlap"]

        print(f"\nTesting chunk_size={chunk_size}, overlap={chunk_overlap}")

        chunks = create_chunks_custom(documents, chunk_size, chunk_overlap)
        index, embeddings = build_index(chunks, model)

        query_results = []

        for item in EVAL_QUERIES:
            retrieved, retrieval_ms = retrieve_custom(
                item["query"], model, index, chunks, k=3
            )

            retrieved_sources = [r["source"] for r in retrieved]

            p1 = precision_at_k(retrieved_sources, item["relevant_sources"], 1)
            p3 = precision_at_k(retrieved_sources, item["relevant_sources"], 3)
            r3 = recall_at_k(retrieved_sources, item["relevant_sources"], 3)

            query_results.append(
                {
                    "query": item["query"],
                    "retrieved_sources": retrieved_sources,
                    "precision_at_1": round(p1, 3),
                    "precision_at_3": round(p3, 3),
                    "recall_at_3": round(r3, 3),
                    "retrieval_ms": round(retrieval_ms, 2),
                }
            )

        avg_p1 = sum(r["precision_at_1"] for r in query_results) / len(query_results)
        avg_p3 = sum(r["precision_at_3"] for r in query_results) / len(query_results)
        avg_r3 = sum(r["recall_at_3"] for r in query_results) / len(query_results)
        avg_latency = sum(r["retrieval_ms"] for r in query_results) / len(query_results)

        summary = {
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "num_chunks": len(chunks),
            "embedding_shape": list(embeddings.shape),
            "average_precision_at_1": round(avg_p1, 3),
            "average_precision_at_3": round(avg_p3, 3),
            "average_recall_at_3": round(avg_r3, 3),
            "average_retrieval_ms": round(avg_latency, 2),
        }

        all_results.append(
            {
                "summary": summary,
                "query_results": query_results,
            }
        )

        print(json.dumps(summary, indent=2))

    output_path = Path("logs/chunking_comparison.json")
    output_path.write_text(json.dumps(all_results, indent=2), encoding="utf-8")

    print("\n" + "=" * 60)
    print("CHUNKING COMPARISON COMPLETE")
    print("=" * 60)
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()