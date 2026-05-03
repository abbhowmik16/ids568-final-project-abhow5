from src.rag_pipeline import (
    DATA_DIR,
    load_documents,
    create_chunks,
    build_embeddings,
    build_faiss_index,
    run_single_query,
)

print("Building RAG test pipeline...")

documents = load_documents(DATA_DIR)
chunks = create_chunks(documents)
model, embeddings = build_embeddings(chunks)
index = build_faiss_index(embeddings)

print(f"Documents loaded: {len(documents)}")
print(f"Chunks created: {len(chunks)}")
print(f"Embedding shape: {embeddings.shape}")
print(f"FAISS index size: {index.ntotal}")

query = "What is retrieval augmented generation?"

result = run_single_query(query, model, index, chunks, k=3)

print("\n=== QUERY ===")
print(result["query"])

print("\n=== RETRIEVED SOURCES ===")
print(result["retrieved_sources"])

print("\n=== LATENCY ===")
print(f"Retrieval ms: {result['retrieval_ms']}")
print(f"Generation ms: {result['generation_ms']}")
print(f"Total ms: {result['total_ms']}")

print("\n=== ANSWER ===")
print(result["answer"])