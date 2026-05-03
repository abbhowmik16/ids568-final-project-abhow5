from pathlib import Path
import subprocess
import time
import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


DATA_DIR = Path("data")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
OLLAMA_PATH = r"C:\Users\Owner\AppData\Local\Programs\Ollama\ollama.exe"
OLLAMA_MODEL = "mistral:7b-instruct"


def load_documents(data_dir: Path) -> list[dict]:
    documents = []

    for file_path in sorted(data_dir.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8").strip()
        documents.append(
            {
                "source": file_path.name,
                "text": text
            }
        )

    return documents


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> list[str]:
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


def create_chunks(documents: list[dict]) -> list[dict]:
    all_chunks = []

    for doc in documents:
        doc_chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(doc_chunks):
            all_chunks.append(
                {
                    "source": doc["source"],
                    "chunk_id": i,
                    "content": chunk
                }
            )

    return all_chunks


def build_embeddings(chunks: list[dict], model_name: str = EMBEDDING_MODEL_NAME):
    model = SentenceTransformer(model_name)
    texts = [chunk["content"] for chunk in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True)
    embeddings = embeddings.astype("float32")
    return model, embeddings


def build_faiss_index(embeddings: np.ndarray):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index


def retrieve(query: str, model, index, chunks: list[dict], k: int = 3):
    start_time = time.time()

    query_embedding = model.encode([query], convert_to_numpy=True).astype("float32")
    distances, indices = index.search(query_embedding, k)

    retrieval_ms = (time.time() - start_time) * 1000

    results = []
    for rank, idx in enumerate(indices[0], start=1):
        chunk = chunks[idx]
        results.append(
            {
                "rank": rank,
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
                "distance": float(distances[0][rank - 1]),
                "content": chunk["content"]
            }
        )

    return results, retrieval_ms


def build_prompt(query: str, retrieved_chunks: list[dict]) -> str:
    context_blocks = []

    for item in retrieved_chunks:
        context_blocks.append(
            f"Source: {item['source']} | Chunk: {item['chunk_id']}\n{item['content']}"
        )

    context = "\n\n".join(context_blocks)

    prompt = f"""You are a helpful assistant answering only from the provided context.

Use only the context below to answer the question.
If the answer is not supported by the context, say: "I do not know based on the provided documents."

Context:
{context}

Question:
{query}

Answer:"""

    return prompt


def generate_with_ollama(prompt: str):
    start_time = time.time()

    result = subprocess.run(
        [OLLAMA_PATH, "run", OLLAMA_MODEL, prompt],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    generation_ms = (time.time() - start_time) * 1000

    if result.returncode != 0:
        raise RuntimeError(f"Ollama error: {result.stderr}")

    return result.stdout.strip(), generation_ms


def run_single_query(query: str, model, index, chunks: list[dict], k: int = 3) -> dict:
    total_start = time.time()

    retrieved_chunks, retrieval_ms = retrieve(query, model, index, chunks, k=k)
    prompt = build_prompt(query, retrieved_chunks)
    answer, generation_ms = generate_with_ollama(prompt)
    total_ms = (time.time() - total_start) * 1000

    return {
        "query": query,
        "retrieved_sources": [item["source"] for item in retrieved_chunks],
        "retrieved_chunk_ids": [item["chunk_id"] for item in retrieved_chunks],
        "answer": answer,
        "retrieval_ms": round(retrieval_ms, 2),
        "generation_ms": round(generation_ms, 2),
        "total_ms": round(total_ms, 2)
    }


def main():
    print("=" * 60)
    print("BUILDING RAG PIPELINE")
    print("=" * 60)

    documents = load_documents(DATA_DIR)
    chunks = create_chunks(documents)
    model, embeddings = build_embeddings(chunks)
    index = build_faiss_index(embeddings)

    print(f"Loaded documents: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Embedding shape: {embeddings.shape}")
    print(f"FAISS vectors: {index.ntotal}")

    evaluation_queries = [
        "What is RAG and how does it work?",
        "Why is chunking important in a RAG pipeline?",
        "What is the role of a vector database?",
        "How do embeddings help retrieval?",
        "What does grounding mean in RAG?",
        "How should RAG evaluation be done?",
        "What happens if retrieval returns irrelevant chunks?",
        "What are the main steps in a RAG pipeline?",
        "Why is chunk overlap useful?",
        "What is the deadline for Milestone 6?"
    ]

    results = []

    print("\n" + "=" * 60)
    print("RUNNING RAG EVALUATION")
    print("=" * 60)

    for i, query in enumerate(evaluation_queries, start=1):
        print(f"\nQuery {i}/10: {query}")
        result = run_single_query(query, model, index, chunks, k=3)
        results.append(result)

        print(f"Retrieved sources: {result['retrieved_sources']}")
        print(f"Retrieval ms: {result['retrieval_ms']}")
        print(f"Generation ms: {result['generation_ms']}")
        print(f"Total ms: {result['total_ms']}")
        print(f"Answer preview: {result['answer'][:180].replace(chr(10), ' ')}...")

    output_path = Path("rag_eval_results.json")
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    avg_retrieval = sum(r["retrieval_ms"] for r in results) / len(results)
    avg_generation = sum(r["generation_ms"] for r in results) / len(results)
    avg_total = sum(r["total_ms"] for r in results) / len(results)

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Saved results to: {output_path}")
    print(f"Average retrieval latency: {avg_retrieval:.2f} ms")
    print(f"Average generation latency: {avg_generation:.2f} ms")
    print(f"Average end-to-end latency: {avg_total:.2f} ms")

    print("\nRAG Step 5 complete: 10-query evaluation finished successfully.")


if __name__ == "__main__":
    main()