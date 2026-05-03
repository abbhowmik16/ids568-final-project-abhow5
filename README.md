IDS568 Final Project: Production Monitoring, Experimentation, and AI Governance



\# Overview



This project extends a Milestone 6 RAG system into a production-ready ML system with monitoring, experimentation, drift detection, and governance controls. The system retrieves information from a small document collection, optionally generates responses using a local LLM, and exposes metrics for observability. The project demonstrates how to operate, evaluate, and govern ML systems in production.



\# System Architecture



Documents → Chunking → Embeddings → FAISS Index → Retrieval → Prompt → Generation → API → Monitoring → Governance



\- Documents: 5 course text files  

\- Chunking: 500 size, 50 overlap  

\- Embedding: MiniLM  

\- Index: FAISS  

\- Generation: Ollama (Mistral)  

\- API: FastAPI  

\- Monitoring: Prometheus  



\# Component 1: Monitoring



\##Features

\- FastAPI service with `/health`, `/ask`, `/metrics`

\- Prometheus metrics instrumentation

\- Traffic simulation (49 requests)

\- Dashboard JSON for Grafana



\##Key Metrics

\- `rag\_requests\_total`

\- `rag\_request\_latency\_seconds`

\- `rag\_retrieval\_latency\_seconds`

\- `rag\_average\_retrieval\_distance`

\- `rag\_response\_length\_chars`



\##Findings

\- Retrieval latency is fast (< 50ms)

\- Generation latency is high (\~80 seconds)

\- Retrieval distance is a useful quality proxy



\# Component 2: A/B Testing



\##Experiment

\- Control: top-k = 3  

\- Treatment: top-k = 5  



\##Results



| Metric | Value |

|---|---|

| Control completion rate | 72.59% |

| Treatment completion rate | 76.73% |

| Relative lift | +5.71% |

| p-value | 0.0000019 |

| Recommendation | Ship Treatment |



\##Guardrails

\- Latency p99 < 3s → Passed  

\- Error rate threshold → Passed  



\# Component 3: Governance Documentation



\##Artifacts

\- System card (model-card.md)

\- Audit trail (logs/audit\_trail.json)

\- Lineage diagram (docs/lineage-diagram.md)



\##Key Points

\- System is retrieval-based, not trained model

\- Knowledge base is small (5 docs)

\- Monitoring and audit tracking are implemented



\#Component 4: Drift Detection



\##Signals Monitored

\- Query length

\- Retrieval distance

\- Response length



\##Results



| Feature | PSI | Severity |

|---|---|---|

| Query length | 2.748 | Significant |

| Retrieval distance | 1.669 | Significant |

| Response length | 0.760 | Significant |



\##Insight

\- Drift suggests queries are becoming more complex

\- Retrieval quality may degrade over time



\#Component 5: Risk \& Compliance



\##Key Risks

\- Hallucination

\- Weak retrieval

\- Latency

\- Prompt injection

\- Data exposure



\##Mitigation

\- Monitor retrieval distance

\- Require grounded answers

\- Add fallback responses

\- Maintain audit trail



\# Repository Structure



src/

monitoring/

ab\_test/

drift/

docs/

logs/

dashboards/

visualizations/

screenshots/

config/



\#How to Run



\##1. Activate environment

.venv\\Scripts\\Activate.ps1



\##2. Run API

uvicorn src.monitoring.instrumented\_rag\_service:app --reload





\##3. Test endpoints

/health

/ask?q=What is RAG

/metrics



\#Key Learnings



1\. Monitoring is essential for ML systems in production  

2\. Retrieval quality can be measured using precision@k and recall@k  

3\. Drift detection can use simple statistical techniques like PSI  

4\. Governance requires documentation, audit trails, and risk analysis  

5\. Latency and retrieval quality are the main operational trade-offs  



\#Conclusion



This project demonstrates a full ML lifecycle beyond model building, including monitoring, experimentation, drift detection, and governance. The system is not production-ready for real-world deployment due to its small knowledge base and high latency, but it provides a strong framework for managing ML systems responsibly.

