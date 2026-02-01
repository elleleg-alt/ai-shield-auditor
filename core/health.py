"""
Health check and monitoring utilities
"""
import os
import sys
from typing import Dict, Any
from datetime import datetime
import platform


def get_health_status() -> Dict[str, Any]:
    """
    Get application health status

    Returns:
        Dictionary containing health information
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0",
        "python_version": sys.version.split()[0],
        "platform": platform.system(),
        "environment": os.getenv("ENV", "production"),
    }


def check_dependencies() -> Dict[str, bool]:
    """
    Check if all required dependencies are available

    Returns:
        Dictionary mapping dependency names to availability status
    """
    dependencies = {
        "streamlit": False,
        "pydantic": False,
        "pandas": False,
        "reportlab": False,
    }

    for dep in dependencies:
        try:
            __import__(dep)
            dependencies[dep] = True
        except ImportError:
            dependencies[dep] = False

    return dependencies


def check_llm_providers() -> Dict[str, bool]:
    """
    Check if LLM provider API keys are configured

    Returns:
        Dictionary mapping provider names to configuration status
    """
    return {
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
        "active_provider": os.getenv("LLM_PROVIDER", "none"),
    }


def get_system_metrics() -> Dict[str, Any]:
    """
    Get system metrics (basic version without psutil)

    Returns:
        Dictionary containing basic system information
    """
    try:
        import psutil
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
        }
    except ImportError:
        # Fallback if psutil not available
        return {
            "cpu_percent": "N/A (psutil not installed)",
            "memory_percent": "N/A (psutil not installed)",
            "disk_percent": "N/A (psutil not installed)",
        }
