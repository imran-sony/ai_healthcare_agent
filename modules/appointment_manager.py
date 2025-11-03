# modules/appointment_manager.py
import uuid
from datetime import datetime

def schedule_appointment(text, context):
    booking_id = str(uuid.uuid4())
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    context["last_appointment"] = {"id": booking_id, "time": now}
    return f"Appointment scheduled at {now}, booking ID: {booking_id}."

