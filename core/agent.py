# core/agent.py
from core.pipeline import process_message
from core.state_manager import SessionManager
from utils.config import CONFIG
from modules.medical_qa import AsyncGroq

class HealthcareAgent:
    def __init__(self):
        self.sessions = SessionManager()
        self.model_name = CONFIG["MODEL_NAME"]
        self.groq = self._init_groq_client()

    def _init_groq_client(self):
        key = CONFIG["GROQ_API_KEY"]
        if not key:
            print("Warning: GROQ_API_KEY is empty. LLM calls will fail.")
            return None

        if AsyncGroq:
            try:
                return AsyncGroq(api_key=key)
            except Exception as e:
                print("AsyncGroq client init failed:", e)
                return None

        print("AsyncGroq SDK not available.")
        return None

    async def run(self, text: str, session_id: str) -> dict:
        context = self.sessions.get_session(session_id)
        response, updated_context = await process_message(
            text, context, groq_client=self.groq, model_name=self.model_name
        )
        self.sessions.save_session(session_id, updated_context)
        return response
