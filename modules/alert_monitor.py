# modules/alert_monitor.py
def check_emergency(risk_level: str) -> bool:
    """Return True if high-risk symptoms detected."""
    return risk_level.lower() == "high"
