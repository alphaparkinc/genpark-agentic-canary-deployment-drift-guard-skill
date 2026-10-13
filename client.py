"""
Agentic Canary Deployment Drift & Metric Regression Guard (Zero External Dependencies)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import json
import math
from typing import Dict, Any, List

class AgenticCanaryDeploymentDriftGuard:
    def __init__(self, guard_name: str = "GenPark Canary Sentinel"):
        self.guard_name = guard_name

    def compute_stats(self, values: List[float]) -> Dict[str, float]:
        if not values:
            return {"mean": 0.0, "variance": 0.0, "std_dev": 0.0, "n": 0}
        n = len(values)
        mean = sum(values) / n
        if n == 1:
            return {"mean": mean, "variance": 0.0, "std_dev": 0.0, "n": 1}
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        return {"mean": mean, "variance": variance, "std_dev": math.sqrt(variance), "n": n}

    def welch_t_statistic(self, s1: Dict[str, float], s2: Dict[str, float]) -> float:
        n1, v1 = s1["n"], s1["variance"]
        n2, v2 = s2["n"], s2["variance"]
        if n1 < 2 or n2 < 2:
            return 0.0
        denom = math.sqrt((v1 / n1) + (v2 / n2))
        if denom == 0.0:
            return 0.0
        return (s2["mean"] - s1["mean"]) / denom

    def evaluate_canary_health(self, baseline_metrics: Dict[str, List[float]], canary_metrics: Dict[str, List[float]]) -> Dict[str, Any]:
        violations = []
        metrics_checked = ["latency_ms", "error_rate", "hallucination_score"]
        comparison_results = {}
        rollback_required = False
        
        for m in metrics_checked:
            b_vals = baseline_metrics.get(m, [100.0, 105.0, 95.0, 102.0])
            c_vals = canary_metrics.get(m, [100.0, 105.0, 95.0, 102.0])
            
            b_stats = self.compute_stats(b_vals)
            c_stats = self.compute_stats(c_vals)
            t_val = self.welch_t_statistic(b_stats, c_stats)
            
            relative_delta = 0.0
            if b_stats["mean"] > 0:
                relative_delta = round(((c_stats["mean"] - b_stats["mean"]) / b_stats["mean"]) * 100.0, 2)
                
            is_degraded = (t_val > 2.0 and relative_delta > 5.0) or (m == "error_rate" and c_stats["mean"] > 0.05)
            if is_degraded:
                rollback_required = True
                violations.append(f"Metric '{m}' drifted significantly: t={t_val:.2f}, delta=+{relative_delta}%")
                
            comparison_results[m] = {
                "baseline_mean": round(b_stats["mean"], 3),
                "canary_mean": round(c_stats["mean"], 3),
                "welch_t_stat": round(t_val, 2),
                "percentage_delta": relative_delta,
                "status": "DEGRADED" if is_degraded else "HEALTHY"
            }
            
        return {
            "sentinel": self.guard_name,
            "overall_decision": "ROLLBACK_ABORT_CANARY" if rollback_required else "PROMOTE_CANARY_TRAFFIC",
            "rollback_required": rollback_required,
            "violations_detected": violations,
            "metrics_breakdown": comparison_results,
            "recommended_action": "Execute immediate traffic cutback to vBaseline" if rollback_required else "Increase traffic split to 50%"
        }
