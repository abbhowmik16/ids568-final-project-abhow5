\# Drift Detection Diagnostic Report



\*\*System:\*\* IDS568 Final Project RAG System  

\*\*Analysis Type:\*\* Simulated RAG observable drift  

\*\*Prepared by:\*\* Keya Debnath  



\## Executive Summary



The drift analysis shows significant distribution shift across all three monitored RAG signals: query length, retrieval distance, and response length. The most important operational concern is the increase in retrieval distance from 0.754 to 1.048, because higher FAISS distance indicates weaker semantic similarity between user queries and indexed documents.



Overall drift status: \*\*Significant Drift\*\*



Recommended action: investigate recent query patterns, refresh the knowledge base, and continue monitoring retrieval distance as an early warning signal.



\## Drift Results



| Feature | Reference Mean | Current Mean | PSI | Severity |

|---|---:|---:|---:|---|

| Query length tokens | 8.014 | 13.100 | 2.748 | Significant |

| Retrieval distance | 0.754 | 1.048 | 1.669 | Significant |

| Response length chars | 184.882 | 261.623 | 0.760 | Significant |



\## Most Affected Features



\### Query Length Tokens



Query length increased from 8.014 to 13.100 tokens. This suggests users are asking longer or more complex questions than the reference period. Longer questions can reduce retrieval precision if the embedding model struggles to represent multi-part requests.



\### Retrieval Distance



Retrieval distance increased from 0.754 to 1.048. This is the most important drift signal because it indicates that retrieved chunks are less semantically close to current queries. In a RAG system, this can directly reduce answer groundedness.



\### Response Length



Response length increased from 184.882 to 261.623 characters. This may indicate that the model is producing longer responses to compensate for weaker retrieved context. In production, this could increase latency and hallucination risk.



\## Impact on Model/System Performance



The drift pattern suggests a possible knowledge-base coverage gap. If query length rises and retrieval distance also rises, the system is likely receiving questions that are not well covered by the existing indexed documents.



Expected impacts include:



1\. Lower retrieval precision.

2\. Higher risk of unsupported answers.

3\. Increased response length and latency.

4\. Reduced user trust if answers become less grounded.



\## Root Cause Hypotheses



1\. \*\*New query patterns:\*\* Users may be asking broader or more complex questions than those represented in the original five-document knowledge base.

2\. \*\*Small knowledge base:\*\* The current index contains only five documents and 14 chunks, which limits coverage.

3\. \*\*Chunking limitations:\*\* Some answers may require better chunk boundaries or larger context windows.

4\. \*\*Embedding limitations:\*\* The current MiniLM embedding model is lightweight and fast, but may not perform as well on complex semantic matching.



\## Recommended Actions



\### Immediate



1\. Review recent queries with high retrieval distance.

2\. Flag answers generated from weak retrieval context.

3\. Add dashboard alert for average retrieval distance above 1.2.



\### Short Term



1\. Refresh and expand the knowledge base.

2\. Re-run precision@k and recall@k after adding new documents.

3\. Compare retrieval performance using top-k = 3 and top-k = 5.



\### Long Term



1\. Test alternative embedding models.

2\. Schedule regular drift checks.

3\. Connect drift alerts to audit trail events.

4\. Add human review for low-confidence or high-distance retrieval cases.



\## Monitoring Connection



This drift report connects directly to the monitoring dashboard. The dashboard tracks average retrieval distance, retrieved chunk count, and response length. These monitored metrics can detect the same type of degradation analyzed in this report.



\## Conclusion



The system remains functional, but drift analysis shows that retrieval quality can degrade when queries shift away from the indexed knowledge base. The most appropriate response is knowledge base refresh, retrieval evaluation, and continued monitoring rather than immediate model replacement.

