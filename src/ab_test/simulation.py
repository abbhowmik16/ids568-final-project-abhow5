"""
A/B Test Simulation for RAG Retrieval Configuration
Component 2: A/B Test Design & Simulation

Control: top-k = 3
Treatment: top-k = 5
Primary metric: task completion rate
Guardrails: p99 latency and error rate
"""

import json
import hashlib
from pathlib import Path

import numpy as np
from scipy import stats


EXPERIMENT_NAME = "rag_topk_ab_test"
RANDOM_SEED = 42

BASELINE_COMPLETION_RATE = 0.72
TREATMENT_COMPLETION_RATE = 0.755
ALPHA = 0.05
POWER = 0.80
MDE = 0.04

N_USERS = 10000


def assign_variant(user_id: str, experiment_name: str, control_weight: float = 0.5):
    hash_input = f"{user_id}:{experiment_name}"
    hash_value = hashlib.md5(hash_input.encode()).hexdigest()
    hash_float = int(hash_value[:8], 16) / (16**8)
    return "control" if hash_float < control_weight else "treatment"


def calculate_sample_size(baseline_rate, mde, alpha=0.05, power=0.80):
    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde)

    effect_size = 2 * (np.arcsin(np.sqrt(p2)) - np.arcsin(np.sqrt(p1)))

    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)

    n = 2 * ((z_alpha + z_power) / effect_size) ** 2
    return int(np.ceil(n))


def two_proportion_ztest(control_success, control_n, treatment_success, treatment_n):
    p_control = control_success / control_n
    p_treatment = treatment_success / treatment_n

    pooled = (control_success + treatment_success) / (control_n + treatment_n)
    se = np.sqrt(pooled * (1 - pooled) * ((1 / control_n) + (1 / treatment_n)))

    z_stat = (p_treatment - p_control) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    se_diff = np.sqrt(
        p_control * (1 - p_control) / control_n
        + p_treatment * (1 - p_treatment) / treatment_n
    )

    diff = p_treatment - p_control
    ci_low = diff - 1.96 * se_diff
    ci_high = diff + 1.96 * se_diff

    return {
        "control_rate": p_control,
        "treatment_rate": p_treatment,
        "absolute_lift": diff,
        "relative_lift": diff / p_control,
        "z_stat": z_stat,
        "p_value": p_value,
        "ci_95": [ci_low, ci_high],
        "significant": p_value < ALPHA,
    }


def main():
    np.random.seed(RANDOM_SEED)

    required_n = calculate_sample_size(BASELINE_COMPLETION_RATE, MDE, ALPHA, POWER)

    users = []
    for i in range(N_USERS):
        user_id = f"user_{i:05d}"
        variant = assign_variant(user_id, EXPERIMENT_NAME)
        users.append((user_id, variant))

    control_users = [u for u in users if u[1] == "control"]
    treatment_users = [u for u in users if u[1] == "treatment"]

    control_n = len(control_users)
    treatment_n = len(treatment_users)

    control_success = np.random.binomial(control_n, BASELINE_COMPLETION_RATE)
    treatment_success = np.random.binomial(treatment_n, TREATMENT_COMPLETION_RATE)

    stats_result = two_proportion_ztest(
        control_success, control_n, treatment_success, treatment_n
    )

    # Guardrails
    control_latency = np.random.lognormal(mean=np.log(1.4), sigma=0.25, size=control_n)
    treatment_latency = np.random.lognormal(mean=np.log(1.65), sigma=0.25, size=treatment_n)

    control_error_rate = 0.008
    treatment_error_rate = 0.010

    control_errors = np.random.binomial(control_n, control_error_rate)
    treatment_errors = np.random.binomial(treatment_n, treatment_error_rate)

    latency_guardrail = {
        "control_p99_seconds": float(np.percentile(control_latency, 99)),
        "treatment_p99_seconds": float(np.percentile(treatment_latency, 99)),
        "threshold_seconds": 3.0,
        "passed": float(np.percentile(treatment_latency, 99)) <= 3.0,
    }

    error_guardrail = {
        "control_error_rate": control_errors / control_n,
        "treatment_error_rate": treatment_errors / treatment_n,
        "threshold": control_error_rate + 0.005,
        "passed": (treatment_errors / treatment_n) <= (control_error_rate + 0.005),
    }

    guardrails_passed = latency_guardrail["passed"] and error_guardrail["passed"]

    if stats_result["significant"] and stats_result["relative_lift"] > 0 and guardrails_passed:
        recommendation = "SHIP_TREATMENT"
    elif stats_result["significant"] and stats_result["relative_lift"] > 0 and not guardrails_passed:
        recommendation = "INVESTIGATE_GUARDRAILS"
    elif not stats_result["significant"]:
        recommendation = "EXTEND_EXPERIMENT"
    else:
        recommendation = "KEEP_CONTROL"

    output = {
        "experiment_name": EXPERIMENT_NAME,
        "control": "top-k = 3",
        "treatment": "top-k = 5",
        "required_sample_size_per_variant": required_n,
        "actual_control_n": control_n,
        "actual_treatment_n": treatment_n,
        "primary_metric": "task_completion_rate",
        "primary_metric_results": stats_result,
        "guardrails": {
            "latency": latency_guardrail,
            "error_rate": error_guardrail,
        },
        "guardrails_passed": guardrails_passed,
        "recommendation": recommendation,
    }

    Path("logs").mkdir(exist_ok=True)
    Path("logs/ab_test_results.json").write_text(
        json.dumps(output, indent=2, default=str), encoding="utf-8"
    )

    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()