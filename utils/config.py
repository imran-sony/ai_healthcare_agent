# utils/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

CONFIG = {
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
    "MODEL_NAME": os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"),
    "REDIS_URL": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    "MAX_CONCURRENT_GROQ": int(os.getenv("MAX_CONCURRENT_GROQ", "4")),
    "RAG_TOP_K": int(os.getenv("RAG_TOP_K", "1")),
    "DEBUG": os.getenv("DEBUG", "false").lower() == "true",
}
