# genpark-agentic-canary-deployment-drift-guard-skill

[![Official Hub](https://img.shields.io/badge/GenPark-Official%20Hub-6366f1?style=for-the-badge&logo=compass&logoColor=white)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/92955550)
[![Zero External Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Pure%20Stdlib)-success?style=for-the-badge)](https://www.genpark.ai)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-blue?style=for-the-badge)](https://www.genpark.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)  
> **LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) ([https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550))

Agentic Canary Deployment Drift & Metric Regression Guard. Conducts Welch's t-test statistical hypothesis testing between baseline and canary agent versions across P99 latency, error rates, and hallucination scores to execute instant automated rollback circuit breakers.

---

## 🌐 Official GenPark AI Ecosystem Links

- **GenPark Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Official Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) ([https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550))

---

## 🌟 Key Features

- **100% Zero External Dependencies**: Runs entirely on the Python 3.9+ standard library.
- **Model Context Protocol (MCP) Standard**: Native support for JSON-RPC 2.0 `initialize`, `tools/list`, and `tools/call`.
- **Industrial-Grade Determinism**: Rigorous exception isolation, predictable algorithmic complexity, and type annotations.
- **Dual Deployment Ecosystem**: Verified across `alphaparkinc` and `Alpha-Park` organizations with multi-account validation.

---

## 🚀 Quick Start

### 1. Direct Python SDK Usage

```python
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

```

### 2. Run as Model Context Protocol (MCP) Server

Start standard JSON-RPC 2.0 server over `stdio`:

```bash
python mcp_server.py
```

Execute embedded test harness:

```bash
python mcp_server.py --test
```

---

## 🛠️ MCP Tool Specification

Inspect [`skill.json`](skill.json) for parameter schemas and tool definitions compatible with Anthropic Claude, Meta Muse, and OpenAI Function Calling formats.

---

## 📜 License & Community

Licensed under the [MIT License](LICENSE). Copyright © 2026 [GenPark AI](https://www.genpark.ai).
Follow us on LinkedIn: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550) | [https://www.llinkedin.com/company/92955550](https://www.llinkedin.com/company/92955550)
