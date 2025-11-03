# modules/symptom_checker.py
def check_symptoms(text):
    high_risk = ["chest pain", "shortness of breath", "severe headache", "fainting", "rapid heart"]
    medium_risk = ["fever", "cough", "fatigue", "nausea", "vomiting"]

    risk = "low"
    reply = "Symptoms noted."
    text_lower = text.lower()

    if any(hr in text_lower for hr in high_risk):
        risk = "high"
        reply = "High-risk symptoms detected."
    elif any(mr in text_lower for mr in medium_risk):
        risk = "medium"
        reply = "Moderate symptoms detected."

    return risk, reply
