# core/pipeline.py
from modules.symptom_checker import check_symptoms
from modules.alert_monitor import check_emergency
from modules.appointment_manager import schedule_appointment
from modules.medical_qa import answer_medical_question

async def process_message(text, context, groq_client=None, model_name=None):
    text_lower = text.lower()

    if "appointment" in text_lower:
        intent = "appointment"
        reply = schedule_appointment(text, context)
        sources = []

    elif any(symptom in text_lower for symptom in ["pain", "fever", "cough", "headache", "nausea"]):
        intent = "symptom_check"
        risk, _ = check_symptoms(text)

        prompt = (
            "The user is asking about symptoms. Provide a clear, concise explanation of typical signs, "
            "self-care advice, warning signs that need urgent care, and a brief next step. "
            f"Question: {text}"
        )

        reply, sources = await answer_medical_question(prompt, groq_client=groq_client, model_name=model_name)

        if check_emergency(risk):
            reply += " This may be an emergency — seek urgent medical attention or call emergency services."

    else:
        intent = "medical_info"
        reply, sources = await answer_medical_question(text, groq_client=groq_client, model_name=model_name)

    # maintain last 20 messages
    history = context.get("history", [])
    history.append({"user": text, "agent": reply, "intent": intent})
    context["history"] = history[-20:]

    return {"reply": reply, "intent": intent, "sources": sources}, context
