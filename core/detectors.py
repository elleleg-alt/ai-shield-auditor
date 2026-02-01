
from typing import Dict, Any

# Lightweight heuristic detection. In real deployments, enrich with SDK calls, headers, or config scraping.
def detect_environment(user_inputs: Dict[str, Any]) -> Dict[str, Any]:
    platform = user_inputs.get("platform") or "Custom"
    agent_mode = user_inputs.get("agent_mode", False)
    connectors = user_inputs.get("connectors", [])
    vector_store = user_inputs.get("vector_store") or "Unknown"
    return {
        "platform": platform,
        "agent_mode": agent_mode,
        "connectors": connectors,
        "vector_store": vector_store,
    }
