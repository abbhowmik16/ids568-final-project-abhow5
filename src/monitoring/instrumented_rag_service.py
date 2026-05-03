"""
Instrumented RAG Service for Final Project Component 1.
Tracks latency, request count, errors, retrieval count, retrieval distance,
response length, and generation latency using Prometheus metrics.
"""

import sys
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from prometheus_client import Counter, Histogram, Gauge, make_asgi_app

# Allow importing rag_pipeline.py from src/
SRC_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(SRC_DIR))

from rag_pipeline import (
    DATA_DIR,
    load_documents,
    create_chunks,
    build_embeddings,
    build_faiss_index,
    retrieve,
    build_prompt,
    generate_with_ollama,
)

app = FastAPI(title="IDS568 Final Project Instrumented RAG Service")

# -----------------------------
# Prometheus Metrics
# -----------------------------

RAG_REQUESTS = Counter(
    "rag_requests_total",
    "Total RAG requests",
    ["status"]
)

RAG_REQUEST_LATENCY = Histogram(
    "rag_request_latency_seconds",
    "End-to-end RAG request latency",
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, 30, 60, 120]
)

RAG_RETRIEVAL_LATENCY = Histogram(
    "rag_retrieval_latency_seconds",
    "Retriever latency",
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1]
)

RAG_RESULT_COUNT = Histogram(
    "rag_retrieval_result_count",
    "Number of chunks returned",
    buckets=[0, 1, 2, 3, 5, 10]
)

RAG_AVG_DISTANCE = Gauge(
    "rag_average_retrieval_distance",
    "Average FAISS distance for retrieved chunks"
)

RAG_RESPONSE_LENGTH = Histogram(
    "rag_response_length_chars",
    "Generated or simulated response length in characters",
    buckets=[50, 100, 250, 500, 1000, 2000]
)

RAG_GENERATION_LATENCY = Histogram(
    "rag_generation_latency_seconds",
    "Ollama generation latency",
    buckets=[1, 5, 10, 30, 60, 120]
)

# Expose /metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# -----------------------------
# Load RAG pipeline once
# -----------------------------

print("Loading RAG components...")

documents = load_documents(DATA_DIR)
chunks = create_chunks(documents)
model, embeddings = build_embeddings(chunks)
index = build_faiss_index(embeddings)

print(f"Documents loaded: {len(documents)}")
print(f"Chunks created: {len(chunks)}")
print(f"FAISS index size: {index.ntotal}")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "documents": len(documents),
        "chunks": len(chunks),
        "faiss_vectors": index.ntotal,
    }


@app.get("/ask")
def ask(q: str, k: int = 3, generate: Optional[bool] = False):
    start = time.time()

    try:
        retrieved_chunks, retrieval_ms = retrieve(q, model, index, chunks, k=k)

        retrieval_seconds = retrieval_ms / 1000
        RAG_RETRIEVAL_LATENCY.observe(retrieval_seconds)
        RAG_RESULT_COUNT.observe(len(retrieved_chunks))

        if retrieved_chunks:
            avg_distance = sum(item["distance"] for item in retrieved_chunks) / len(retrieved_chunks)
            RAG_AVG_DISTANCE.set(avg_distance)

        if generate:
            prompt = build_prompt(q, retrieved_chunks)
            answer, generation_ms = generate_with_ollama(prompt)
            RAG_GENERATION_LATENCY.observe(generation_ms / 1000)
        else:
            answer = "Generation skipped for monitoring test. Retrieved context is returned as evidence."

        RAG_RESPONSE_LENGTH.observe(len(answer))
        RAG_REQUESTS.labels(status="success").inc()

        return {
            "query": q,
            "generate": generate,
            "retrieved_sources": [item["source"] for item in retrieved_chunks],
            "retrieved_chunk_ids": [item["chunk_id"] for item in retrieved_chunks],
            "retrieval_distances": [round(item["distance"], 4) for item in retrieved_chunks],
            "answer": answer,
            "retrieval_ms": round(retrieval_ms, 2),
            "total_ms": round((time.time() - start) * 1000, 2),
        }

    except Exception as e:
        RAG_REQUESTS.labels(status="error").inc()
        return {"error": str(e)}

    finally:
        RAG_REQUEST_LATENCY.observe(time.time() - start)