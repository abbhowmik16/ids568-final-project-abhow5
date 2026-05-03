\# Experiment Specification: RAG Top-k A/B Test



\## Hypothesis



Increasing retrieval from top-k = 3 to top-k = 5 will improve user task completion by at least 4% relative lift without violating latency or error-rate guardrails.



\## Variants



| Variant | Configuration | Description |

|---|---|---|

| Control | top-k = 3 | Current retrieval configuration |

| Treatment | top-k = 5 | Retrieves more context for answer generation |



\## Primary Metric



\*\*Task completion rate\*\*: percentage of users who receive an answer and do not need to re-query within the simulated session.



This metric is appropriate because RAG quality should be evaluated by whether users receive enough relevant context to complete their task.



\## Guardrail Metrics



| Guardrail | Threshold | Reason |

|---|---:|---|

| p99 latency | Must be <= 3.0 seconds | Prevents retrieval expansion from making the system too slow |

| Error rate | Must not exceed baseline + 0.5 percentage points | Ensures new configuration does not reduce reliability |



\## Randomization Method



Users are assigned using deterministic hashing of `user\_id + experiment\_name`. This ensures sticky assignment, meaning the same user always receives the same variant during the experiment.



Traffic split is 50/50 between control and treatment.



\## Sample Size and Duration



Baseline task completion rate is assumed to be 72%. The minimum detectable effect is 4% relative lift. With alpha = 0.05 and power = 0.80, the required sample size is 3,690 users per variant.



The simulation used 10,000 total users:



| Group | Users |

|---|---:|

| Control | 4,984 |

| Treatment | 5,016 |



This exceeds the required sample size and provides enough statistical power for the simulated decision.



\## Success Criteria



The treatment should be shipped only if:



1\. Task completion improves with p < 0.05.

2\. The confidence interval shows positive practical lift.

3\. Latency p99 remains below 3.0 seconds.

4\. Error rate remains within the allowed threshold.



\## Connection to System Governance



This experiment validates a retrieval configuration change that would also be documented in the system card, audit trail, and monitoring dashboard. If the treatment is shipped, the audit trail should record a retrieval configuration change from top-k = 3 to top-k = 5.

