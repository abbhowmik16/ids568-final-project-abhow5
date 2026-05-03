\# Dashboard Interpretation Report



\## System Overview



This dashboard monitors the IDS568 final project RAG system adapted from Milestone 6. The system loads five course knowledge documents, chunks them into 14 text chunks, embeds them using `sentence-transformers/all-MiniLM-L6-v2`, indexes them with FAISS, and serves retrieval responses through a FastAPI endpoint.



The monitoring service exposes Prometheus metrics at `/metrics`. Simulated traffic was generated using 49 successful RAG requests. The dashboard is designed to monitor operational health, retrieval behavior, and early quality-risk signals.



\## Dashboard Design



The dashboard follows a production monitoring structure:



1\. Total RAG requests

2\. End-to-end latency p95

3\. Retrieval latency p95

4\. Average retrieval distance

5\. Retrieved chunk count

6\. Response length



These metrics were selected because they are directly observable from the RAG service and do not require a separate LLM-as-judge evaluation pipeline.



\## Panel-by-Panel Interpretation



\### Panel 1: Total RAG Requests



\*\*Current State:\*\* The Prometheus snapshot recorded 49 successful RAG requests.



\*\*Analysis:\*\* This confirms that the instrumented FastAPI service is receiving traffic and that requests are being counted correctly. Because all recorded requests were successful, there is no current evidence of service-level failure.



\*\*Health Assessment:\*\* Healthy.



\### Panel 2: End-to-End Latency p95



\*\*Current State:\*\* The service recorded request latency using `rag\_request\_latency\_seconds`.



\*\*Analysis:\*\* During simulated monitoring traffic, generation was disabled to isolate retrieval performance. This produced low end-to-end latency because the service returned retrieved evidence rather than calling Ollama for every request. Earlier standalone testing showed that full Ollama generation can take more than 80 seconds, which is the main production bottleneck.



\*\*Health Assessment:\*\* Healthy for retrieval-only mode, warning for full generation mode.



\### Panel 3: Retrieval Latency p95



\*\*Current State:\*\* Retrieval latency was consistently low across the simulated requests.



\*\*Analysis:\*\* FAISS retrieval over 14 vectors is fast and stable. This indicates that the vector index is not the bottleneck. If retrieval latency increased in production, likely causes would include a much larger index, inefficient embedding generation, or hardware constraints.



\*\*Health Assessment:\*\* Healthy.



\### Panel 4: Average Retrieval Distance



\*\*Current State:\*\* The average FAISS distance was tracked with `rag\_average\_retrieval\_distance`.



\*\*Analysis:\*\* Retrieval distance acts as a quality proxy. A rising average distance would suggest that user queries are becoming less similar to the indexed knowledge base. This would indicate possible knowledge base coverage gaps or query distribution drift.



\*\*Health Assessment:\*\* Healthy but important to monitor.



\### Panel 5: Retrieved Chunk Count



\*\*Current State:\*\* Each request retrieved three chunks.



\*\*Analysis:\*\* A stable retrieved chunk count confirms that the retriever is returning the expected top-k results. A drop toward zero would indicate empty retrieval and should trigger investigation.



\*\*Health Assessment:\*\* Healthy.



\### Panel 6: Response Length



\*\*Current State:\*\* Response length was stable because generation was skipped during monitoring traffic.



\*\*Analysis:\*\* In full generation mode, response length can be used as a proxy for generation behavior. Sudden increases may indicate weak retrieved context, causing the LLM to produce longer and less grounded answers.



\*\*Health Assessment:\*\* Healthy for simulation mode.



\## Identified Bottlenecks and Risks



1\. \*\*Ollama generation latency:\*\* The main bottleneck is not retrieval, but local LLM generation. A previous test produced generation latency above 80 seconds. This would be unacceptable for an interactive production system without batching, caching, or a smaller model.



2\. \*\*Small knowledge base:\*\* The system uses only five documents and 14 chunks. This is enough for the course demonstration but creates a high risk of retrieval failure for out-of-domain queries.



3\. \*\*Retrieval quality sensitivity:\*\* Average retrieval distance should be monitored because rising distance may indicate stale or insufficient knowledge base coverage.



4\. \*\*No real-time groundedness metric:\*\* Groundedness requires offline evaluation or human review. It should not be treated as a real-time Prometheus metric.



\## Alert Trigger Recommendations



| Metric | Warning Threshold | Critical Threshold | Rationale |

|---|---:|---:|---|

| End-to-end latency p95 | > 5 seconds | > 30 seconds | High latency affects usability |

| Retrieval latency p95 | > 0.5 seconds | > 1 second | Retrieval should remain fast |

| Error rate | > 1% | > 5% | Indicates service instability |

| Average retrieval distance | > 1.2 | > 1.5 | Indicates weaker semantic match |

| Retrieved chunk count | < 3 average | < 1 average | Indicates retrieval failure |

| Response length | > 500 characters average | > 1000 characters average | May indicate weak grounding or verbose generation |



\## Action Items



1\. Add caching for repeated queries before enabling full generation in production.

2\. Expand the knowledge base to improve coverage.

3\. Monitor retrieval distance over time as a drift signal.

4\. Use offline evaluation for groundedness and hallucination risk.

5\. Set alert thresholds for latency, error rate, and retrieval-distance drift.

