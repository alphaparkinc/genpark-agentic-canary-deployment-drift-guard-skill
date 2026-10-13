#!/usr/bin/env python3
import json
import sys
from client import AgenticCanaryDeploymentDriftGuard

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        guard = AgenticCanaryDeploymentDriftGuard()
        baseline = {"latency_ms": [120.0, 122.0, 118.0, 125.0], "error_rate": [0.01, 0.00, 0.01, 0.00]}
        canary = {"latency_ms": [190.0, 210.0, 195.0, 205.0], "error_rate": [0.08, 0.09, 0.07, 0.08]}
        res = guard.evaluate_canary_health(baseline, canary)
        assert res["rollback_required"] is True
        assert res["overall_decision"] == "ROLLBACK_ABORT_CANARY"
        print(f"[TEST PASS] Canary Drift Guard Alert: {res['overall_decision']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-canary-drift-guard", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "evaluate_canary_health", "description": "Detect canary statistical regression and execute drift guard"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                guard = AgenticCanaryDeploymentDriftGuard()
                out = guard.evaluate_canary_health(args.get("baseline_metrics", {}), args.get("canary_metrics", {}))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
