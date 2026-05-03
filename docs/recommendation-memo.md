\# A/B Test Recommendation Memo



\*\*Experiment:\*\* RAG Top-k Retrieval Comparison  

\*\*Prepared by:\*\* Keya Debnath  

\*\*System:\*\* IDS568 Final Project RAG System  



\## Executive Summary



\*\*Recommendation: Ship Treatment\*\*



The simulated A/B test shows that increasing retrieval from top-k = 3 to top-k = 5 improves task completion rate by 5.71% relative lift, with a statistically significant p-value of 0.0000019. Both latency and error-rate guardrails passed.



\## Experiment Overview



The control configuration used top-k = 3 retrieval. The treatment configuration used top-k = 5 retrieval. The goal was to test whether retrieving more context improves user task completion without making the system too slow or unreliable.



\## Results



| Metric | Control | Treatment | Difference |

|---|---:|---:|---:|

| Task completion rate | 72.59% | 76.73% | +4.14 percentage points |

| Relative lift | — | — | +5.71% |

| p-value | — | — | 0.0000019 |

| 95% CI | — | — | 2.44 to 5.85 percentage points |



\## Guardrail Status



| Guardrail | Control | Treatment | Threshold | Status |

|---|---:|---:|---:|---|

| p99 latency | 2.48 sec | 3.00 sec | <= 3.0 sec | Passed |

| Error rate | 0.80% | 0.98% | <= 1.30% | Passed |



\## Interpretation



The treatment produced a statistically significant and practically meaningful improvement in task completion. The confidence interval is fully positive, which indicates that the observed lift is unlikely to be due to random variation.



The latency guardrail is close to the threshold. Treatment p99 latency was 2.997 seconds, just under the 3.0 second limit. This means the treatment should be shipped with monitoring conditions rather than deployed without oversight.



\## Recommendation



Ship the treatment configuration with top-k = 5, but monitor p99 latency and retrieval distance closely after release.



\## Required Follow-up Actions



1\. Record the configuration change in the audit trail.

2\. Update the system card to document top-k = 5 as the recommended configuration.

3\. Add a dashboard alert if p99 latency exceeds 3.0 seconds.

4\. Continue periodic retrieval evaluation using precision@k and recall@k.

