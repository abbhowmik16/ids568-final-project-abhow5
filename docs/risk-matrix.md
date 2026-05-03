\# Risk Matrix: IDS568 Final Project RAG System



\## Scoring Method



Risk score is calculated as:



\*\*Risk Score = Likelihood × Severity\*\*



| Score | Priority |

|---:|---|

| 1-3 | Low |

| 4-8 | Medium |

| 9-15 | High |

| 16-25 | Critical |



\## Risk Matrix



| Likelihood \\ Severity | 1 Negligible | 2 Minor | 3 Moderate | 4 Major | 5 Critical |

|---|---:|---:|---:|---:|---:|

| 5 Certain | 5 Medium | 10 High | 15 High | 20 Critical | 25 Critical |

| 4 Likely | 4 Medium | 8 Medium | 12 High | 16 Critical | 20 Critical |

| 3 Possible | 3 Low | 6 Medium | 9 High | 12 High | 15 High |

| 2 Unlikely | 2 Low | 4 Medium | 6 Medium | 8 Medium | 10 High |

| 1 Rare | 1 Low | 2 Low | 3 Low | 4 Medium | 5 Medium |



\## System Risks Plotted



| Risk ID | Risk | Likelihood | Severity | Score | Priority |

|---|---|---:|---:|---:|---|

| R001 | Knowledge base staleness | 4 | 3 | 12 | High |

| R002 | Unsupported or hallucinated answer | 3 | 4 | 12 | High |

| R003 | Weak retrieval for complex queries | 4 | 3 | 12 | High |

| R004 | Long generation latency | 4 | 3 | 12 | High |

| R005 | Sensitive data exposure if documents change | 2 | 5 | 10 | High |

| R006 | Prompt injection through user query | 3 | 4 | 12 | High |

| R007 | Tool misuse in agentic workflow | 2 | 4 | 8 | Medium |

| R008 | Lack of human review for weak answers | 3 | 3 | 9 | High |



\## Priority Interpretation



Most risks are high priority because this RAG system combines retrieval, generation, and possible agent-style routing. The highest operational risks are weak retrieval, hallucination, latency, and prompt injection.



\## Mitigation Summary



| Risk Area | Mitigation |

|---|---|

| Retrieval quality | Monitor retrieval distance, evaluate precision@k and recall@k |

| Hallucination | Require context-grounded answer and fallback response |

| Latency | Add caching, monitor p95/p99, consider smaller model |

| Privacy | Review documents before indexing and avoid PII |

| Prompt injection | Add input validation and strict system prompt |

| Accountability | Human review for weak retrieval cases |

