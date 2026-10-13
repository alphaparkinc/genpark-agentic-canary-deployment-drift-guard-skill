from client import AgenticCanaryDeploymentDriftGuard

def main():
    guard = AgenticCanaryDeploymentDriftGuard()
    baseline = {
        "latency_ms": [85.0, 88.0, 92.0, 87.0, 89.0],
        "error_rate": [0.005, 0.002, 0.004, 0.003],
        "hallucination_score": [0.02, 0.03, 0.01, 0.02]
    }
    canary = {
        "latency_ms": [86.0, 87.0, 90.0, 88.0, 88.5],
        "error_rate": [0.004, 0.003, 0.002, 0.003],
        "hallucination_score": [0.02, 0.01, 0.02, 0.02]
    }
    res = guard.evaluate_canary_health(baseline, canary)
    print("--- Canary Deployment Health Evaluation ---")
    print(f"Decision: {res['overall_decision']}")
    print(f"Action: {res['recommended_action']}")
    for k, v in res['metrics_breakdown'].items():
        print(f"  - {k}: Base={v['baseline_mean']} vs Canary={v['canary_mean']} (Delta: {v['percentage_delta']}%, Status: {v['status']})")

if __name__ == "__main__":
    main()
