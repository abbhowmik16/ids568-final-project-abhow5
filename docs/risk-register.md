\# Risk Register: IDS568 Final Project RAG System



\## Risk Matrix Summary



| Risk ID | Risk | Category | Likelihood | Severity | Score | Priority | Treatment |

|---|---|---|---:|---:|---:|---|---|

| R001 | Knowledge base staleness | Robustness | 4 | 3 | 12 | High | Mitigate |

| R002 | Unsupported or hallucinated answer | Safety | 3 | 4 | 12 | High | Mitigate |

| R003 | Weak retrieval for complex queries | Robustness | 4 | 3 | 12 | High | Mitigate |

| R004 | Long generation latency | Reliability | 4 | 3 | 12 | High | Mitigate |

| R005 | Sensitive data exposure if documents change | Privacy | 2 | 5 | 10 | High | Mitigate |

| R006 | Prompt injection through user query | Security | 3 | 4 | 12 | High | Mitigate |

| R007 | Tool misuse in agentic workflow | Security | 2 | 4 | 8 | Medium | Mitigate |

| R008 | Lack of human review for weak answers | Accountability | 3 | 3 | 9 | High | Mitigate |



\## Detailed Risks



\### R001: Knowledge Base Staleness



\*\*Category:\*\* Robustness  

\*\*Likelihood:\*\* 4  

\*\*Severity:\*\* 3  

\*\*Score:\*\* 12  

\*\*Priority:\*\* High  



\*\*Description:\*\* The RAG system may provide outdated or incomplete answers if the indexed documents are not refreshed.



\*\*Potential Harm:\*\* Users may rely on stale or incomplete information.



\*\*Mitigation:\*\*



1\. Schedule knowledge base refresh.

2\. Track document age.

3\. Monitor retrieval distance.

4\. Trigger review when retrieval distance rises above threshold.



\*\*Review Trigger:\*\* Average retrieval distance above 1.2 or no document refresh for 30 days.



\---



\### R002: Unsupported or Hallucinated Answer



\*\*Category:\*\* Safety  

\*\*Likelihood:\*\* 3  

\*\*Severity:\*\* 4  

\*\*Score:\*\* 12  

\*\*Priority:\*\* High  



\*\*Description:\*\* The LLM may generate plausible but unsupported answers when retrieved context is weak.



\*\*Potential Harm:\*\* User receives incorrect answer with high confidence.



\*\*Mitigation:\*\*



1\. Require answers to use retrieved context.

2\. Add fallback response for weak retrieval.

3\. Use offline groundedness evaluation.

4\. Review responses with high retrieval distance.



\*\*Review Trigger:\*\* Retrieval distance above 1.5 or user reports unsupported answer.



\---



\### R003: Weak Retrieval for Complex Queries



\*\*Category:\*\* Robustness  

\*\*Likelihood:\*\* 4  

\*\*Severity:\*\* 3  

\*\*Score:\*\* 12  

\*\*Priority:\*\* High  



\*\*Description:\*\* Longer or multi-topic queries may retrieve less relevant chunks.



\*\*Potential Harm:\*\* Lower precision, weaker answer quality, and higher re-query rate.



\*\*Mitigation:\*\*



1\. Monitor query length drift.

2\. Compare chunk sizes.

3\. Test top-k = 5 treatment.

4\. Evaluate precision@k and recall@k periodically.



\*\*Review Trigger:\*\* Query length PSI above 0.2 or Precision@3 below 0.5.



\---



\### R004: Long Generation Latency



\*\*Category:\*\* Reliability  

\*\*Likelihood:\*\* 4  

\*\*Severity:\*\* 3  

\*\*Score:\*\* 12  

\*\*Priority:\*\* High  



\*\*Description:\*\* Local Ollama generation can take more than 80 seconds for some requests.



\*\*Potential Harm:\*\* Poor user experience and timeout risk.



\*\*Mitigation:\*\*



1\. Add caching for repeated queries.

2\. Use retrieval-only response for monitoring tests.

3\. Consider smaller generation model.

4\. Track p95 and p99 latency.



\*\*Review Trigger:\*\* p95 latency above 5 seconds or p99 latency above 30 seconds.



\---



\### R005: Sensitive Data Exposure if Documents Change



\*\*Category:\*\* Privacy  

\*\*Likelihood:\*\* 2  

\*\*Severity:\*\* 5  

\*\*Score:\*\* 10  

\*\*Priority:\*\* High  



\*\*Description:\*\* If sensitive files are added to the knowledge base, retrieved context may expose private information.



\*\*Potential Harm:\*\* Privacy violation or accidental disclosure.



\*\*Mitigation:\*\*



1\. Do not index PII.

2\. Add document review before ingestion.

3\. Maintain audit trail for knowledge base updates.

4\. Redact sensitive content before embedding.



\*\*Review Trigger:\*\* Any new document ingestion event.



\---



\### R006: Prompt Injection Through User Query



\*\*Category:\*\* Security  

\*\*Likelihood:\*\* 3  

\*\*Severity:\*\* 4  

\*\*Score:\*\* 12  

\*\*Priority:\*\* High  



\*\*Description:\*\* A user may attempt to override system instructions or force the model to ignore retrieved context.



\*\*Potential Harm:\*\* Unsafe, irrelevant, or policy-violating output.



\*\*Mitigation:\*\*



1\. Keep system prompt strict.

2\. Add input validation.

3\. Refuse out-of-scope instructions.

4\. Log suspicious queries for review.



\*\*Review Trigger:\*\* Any detected instruction override attempt.



\---



\### R007: Tool Misuse in Agentic Workflow



\*\*Category:\*\* Security  

\*\*Likelihood:\*\* 2  

\*\*Severity:\*\* 4  

\*\*Score:\*\* 8  

\*\*Priority:\*\* Medium  



\*\*Description:\*\* If the agent controller is extended with tools, incorrect routing or tool execution may cause unsafe behavior.



\*\*Potential Harm:\*\* Wrong tool use, unsafe outputs, or unintended data access.



\*\*Mitigation:\*\*



1\. Keep tool permissions narrow.

2\. Require explicit tool schemas.

3\. Log every tool call.

4\. Add human review before high-impact tool use.



\*\*Review Trigger:\*\* Any failed or unexpected tool execution.



\---



\### R008: Lack of Human Review for Weak Answers



\*\*Category:\*\* Accountability  

\*\*Likelihood:\*\* 3  

\*\*Severity:\*\* 3  

\*\*Score:\*\* 9  

\*\*Priority:\*\* High  



\*\*Description:\*\* The system currently has no formal human review process for weak retrieval or uncertain answers.



\*\*Potential Harm:\*\* Low-quality output reaches users without escalation.



\*\*Mitigation:\*\*



1\. Add human review for high-distance retrieval.

2\. Provide fallback when evidence is insufficient.

3\. Maintain audit logs.

4\. Include escalation rules in governance review.



\*\*Review Trigger:\*\* Retrieval distance above 1.5 or repeated user query within a short session.

