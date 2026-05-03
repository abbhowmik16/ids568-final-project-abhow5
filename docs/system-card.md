\# System Card: IDS568 Final Project RAG System



\## System Details



| Field | Description |

|---|---|

| System Name | IDS568 Final Project RAG System |

| Version | 1.0.0 |

| System Type | Retrieval-Augmented Generation system |

| Base Project | Milestone 6 RAG pipeline and agent controller |

| Owner | Keya Debnath |

| Frameworks | Python, FAISS, SentenceTransformers, FastAPI, Prometheus |

| Embedding Model | sentence-transformers/all-MiniLM-L6-v2 |

| Vector Index | FAISS IndexFlatL2 |

| Generation Model | mistral:7b-instruct through local Ollama |

| Monitoring | Prometheus metrics exposed through FastAPI `/metrics` endpoint |



\## Intended Use



The system is intended for answering questions about course-provided RAG and MLOps learning materials. It retrieves relevant chunks from a small local document collection and can generate an answer using the retrieved context.



\## Intended Users



1\. IDS568 course evaluator.

2\. Student developer testing RAG monitoring and governance.

3\. Technical reviewer evaluating MLOps production-readiness artifacts.



\## Out-of-Scope Uses



The system should not be used for:



1\. Legal, medical, financial, or high-stakes advice.

2\. Production deployment with real user data.

3\. Decisions affecting people or services.

4\. Questions outside the indexed course documents.

5\. Sensitive or confidential information retrieval.



\## System Configuration



| Parameter | Value |

|---|---|

| Documents | 5 text files |

| Default Chunk Size | 500 characters |

| Default Chunk Overlap | 50 characters |

| Total Chunks | 14 |

| Embedding Dimension | 384 |

| Default Retrieval Top-k | 3 |

| A/B Treatment Top-k | 5 |

| Vector Distance Metric | L2 distance |

| Generation Mode | Local Ollama call |

| Monitoring Mode | Prometheus metrics |



\## Training Data / Knowledge Base Description



This system does not train a new LLM. It uses a local knowledge base made of five course-related text files:



1\. `rag\_basics.txt`

2\. `chunking.txt`

3\. `embeddings.txt`

4\. `vector\_databases.txt`

5\. `grounding\_evaluation.txt`



The knowledge base is small and instructional. It is appropriate for demonstrating RAG architecture, retrieval evaluation, monitoring, drift detection, and governance workflows.



\## Performance Metrics



\### Retrieval Evaluation



| Metric | Value |

|---|---:|

| Average Precision@1 | 0.600 |

| Average Precision@3 | 0.600 |

| Average Recall@3 | 1.000 |

| Evaluation Queries | 5 |



\### Chunking Comparison



| Chunk Size | Overlap | Chunks | Precision@1 | Precision@3 | Recall@3 | Avg Retrieval ms |

|---:|---:|---:|---:|---:|---:|---:|

| 300 | 30 | 21 | 0.600 | 0.533 | 1.000 | 9.72 |

| 500 | 50 | 14 | 0.600 | 0.600 | 1.000 | 9.07 |

| 800 | 80 | 10 | 0.800 | 0.467 | 1.000 | 7.11 |



The 500-character chunk size is retained as the default because it provides the best Precision@3 while maintaining full Recall@3.



\### Monitoring Metrics



The instrumented service tracks:



1\. `rag\_requests\_total`

2\. `rag\_request\_latency\_seconds`

3\. `rag\_retrieval\_latency\_seconds`

4\. `rag\_retrieval\_result\_count`

5\. `rag\_average\_retrieval\_distance`

6\. `rag\_response\_length\_chars`

7\. `rag\_generation\_latency\_seconds`



\## A/B Test Summary



The A/B simulation compared top-k = 3 against top-k = 5. The treatment improved simulated task completion from 72.59% to 76.73%, producing a relative lift of 5.71% with p-value 0.0000019. Both latency and error guardrails passed. The recommendation was to ship the treatment with monitoring conditions.



\## Known Limitations



1\. The knowledge base is very small and does not cover broad real-world topics.

2\. Retrieval evaluation uses manually defined relevant source files.

3\. Generation latency is high when Ollama is enabled.

4\. The system currently uses L2 distance with FAISS and does not compare multiple embedding models.

5\. Groundedness is not measured in real time.

6\. The prior Milestone 6 agent routing was keyword-based; this final project focuses on monitoring and governance improvements rather than full LLM-based routing replacement.



\## Failure Modes



| Failure Mode | Likely Cause | Mitigation |

|---|---|---|

| Irrelevant retrieval | Query outside knowledge base | Expand knowledge base and monitor retrieval distance |

| Long latency | Local LLM generation | Add caching, batching, or use smaller model |

| Unsupported answer | Weak retrieved context | Require citations and fallback response |

| Stale answer | Outdated documents | Schedule knowledge base refresh |

| Overly verbose response | Poor retrieval context | Monitor response length and retrieval distance |



\## Ethical Risks



1\. Users may overtrust generated answers.

2\. The system may answer from incomplete course documents.

3\. Poor retrieval may lead to unsupported generation.

4\. If sensitive documents were added later, retrieval could expose private content.



\## Mitigation Strategies



1\. Restrict use to course materials.

2\. Monitor retrieval distance and response length.

3\. Use fallback response when retrieved context is weak.

4\. Keep audit trail for configuration changes.

5\. Do not store PII in the knowledge base.

6\. Use offline groundedness review for high-risk outputs.



\## Governance Notes



This system is documented as a RAG system card rather than a traditional model card because the project does not train the underlying LLM. The documentation focuses on the system configuration, retrieval pipeline, observed performance, operational risks, and monitoring controls.

