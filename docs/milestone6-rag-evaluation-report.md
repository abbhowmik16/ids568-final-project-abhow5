# Milestone 6 Part 1: RAG Evaluation Report

## 1. Overview

This report evaluates a local retrieval-augmented generation (RAG) pipeline built with:
- sentence-transformers/all-MiniLM-L6-v2 for embeddings
- FAISS for vector retrieval
- Ollama with mistral:7b-instruct for grounded answer generation

The document corpus contains 5 local text documents about RAG concepts:
- rag_basics.txt
- vector_databases.txt
- chunking.txt
- embeddings.txt
- grounding_evaluation.txt

The pipeline performs:
1. document ingestion
2. chunking
3. embedding generation
4. FAISS indexing
5. retrieval
6. grounded answer generation

## 2. Chunking and Retrieval Configuration

- Chunking method: fixed-size character chunking
- Chunk size: 500 characters
- Chunk overlap: 50 characters
- Embedding model: sentence-transformers/all-MiniLM-L6-v2
- Vector index: FAISS IndexFlatL2
- Retrieved top-k chunks: 3
- Generator model: mistral:7b-instruct via Ollama

## 3. Evaluation Queries

The following 10 handcrafted queries were used:

1. What is RAG and how does it work?
2. Why is chunking important in a RAG pipeline?
3. What is the role of a vector database?
4. How do embeddings help retrieval?
5. What does grounding mean in RAG?
6. How should RAG evaluation be done?
7. What happens if retrieval returns irrelevant chunks?
8. What are the main steps in a RAG pipeline?
9. Why is chunk overlap useful?
10. What is the deadline for Milestone 6?

## 4. Evaluation Results Table

| Query # | Query | Retrieved Sources Relevant? | Answer Grounded? | Notes |
|---|---|---|---|---|
| 1 | What is RAG and how does it work? | Yes | Yes | Retrieved rag_basics.txt and answer matched the context. |
| 2 | Why is chunking important in a RAG pipeline? | Yes | Yes | Retrieved chunking-related evidence and gave a context-supported explanation. |
| 3 | What is the role of a vector database? | Yes | Yes | Retrieved vector_databases.txt and answer stayed grounded. |
| 4 | How do embeddings help retrieval? | Yes | Yes | Retrieved relevant evidence from embeddings/vector database documents. |
| 5 | What does grounding mean in RAG? | Yes | Yes | Retrieved grounding_evaluation.txt and answered correctly. |
| 6 | How should RAG evaluation be done? | Yes | Yes | Retrieved evaluation-related content and summarized it correctly. |
| 7 | What happens if retrieval returns irrelevant chunks? | Yes | Yes | Retrieved relevant evidence and provided a short grounded answer. |
| 8 | What are the main steps in a RAG pipeline? | Yes | Yes | Retrieved rag_basics.txt and listed pipeline steps correctly. |
| 9 | Why is chunk overlap useful? | Yes | Yes | Retrieved chunking.txt and answered directly from context. |
| 10 | What is the deadline for Milestone 6? | No | Yes | The corpus did not contain the answer, and the model correctly said it did not know. |

## 5. Retrieval Quality Analysis

Retrieval quality was strong for this small domain-specific corpus. For most queries, the top retrieved chunks came from the most relevant source file. In particular:
- queries about RAG basics retrieved rag_basics.txt
- chunking questions retrieved chunking.txt
- vector database questions retrieved vector_databases.txt
- grounding and evaluation questions retrieved grounding_evaluation.txt

This indicates that the embedding model and FAISS index were able to separate the topics reasonably well within the small corpus.

## 6. Grounding Analysis

The generated answers were generally grounded in the retrieved context. The strongest evidence of grounding was Query 10, where the model correctly responded that it did not know based on the provided documents. This shows that the prompt successfully constrained the model to the context instead of encouraging unsupported guessing.

Grounding was also strong for factual and definitional questions because the retrieved chunks clearly contained the answer. No major hallucinated claims were observed in the test outputs.

## 7. Latency Analysis

Observed average latency:
- Average retrieval latency: 23.40 ms
- Average generation latency: 61986.58 ms
- Average end-to-end latency: 62009.98 ms

Retrieval was very fast, while generation was much slower. This is expected because the pipeline was run locally on CPU using a 7B model. The main bottleneck in this system is local text generation, not retrieval.

## 8. Failure Case Analysis

The pipeline handled the out-of-scope query well, but there are still several limitations:

- The corpus is very small and narrow in scope.
- Fixed-size character chunking may split ideas awkwardly.
- Retrieval was evaluated qualitatively, not with a large benchmark.
- Local generation latency is high on CPU.
- Because the corpus is small, the evaluation may overestimate performance compared to a larger, noisier dataset.

## 9. Retrieval Failure vs Generation Failure

This evaluation distinguishes between two failure types:

- Retrieval failure: the wrong chunks are returned for a query
- Generation failure: the correct chunks are retrieved, but the model still gives a misleading or hallucinated answer

In this run, there was no major generation failure visible in the sample outputs. The main risk for this system is future retrieval failure if the corpus becomes larger or more ambiguous.

## 10. Conclusion

The RAG pipeline successfully completed all required stages:
- ingestion
- chunking
- embeddings
- FAISS indexing
- retrieval
- grounded generation
- 10-query evaluation

The system performed well on the small local corpus, with strong relevance and good grounding behavior. The main tradeoff is high generation latency on CPU.