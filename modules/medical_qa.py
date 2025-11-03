# modules/medical_qa.py
import asyncio
from typing import Tuple, List
from retrieval.search import retrieve_knowledge
from utils.config import CONFIG

try:
    from groq import AsyncGroq  
except ImportError:
    AsyncGroq = None

_groq_semaphore = asyncio.Semaphore(CONFIG["MAX_CONCURRENT_GROQ"])

def _build_system_prompt() -> str:
    """
    System prompt for the medical assistant.
    """
    return (
        "You are a cautious, professional virtual medical assistant. "
        "Give general medical information, not diagnoses. "
        "If the user's condition appears serious or life-threatening, "
        "explicitly tell them to seek immediate medical attention. "
        "Cite context when possible and keep the answer concise and empathetic."
    )

async def _call_groq_async(groq_client, prompt: str, model_name: str) -> str:
    """
    Calls the Groq LLM asynchronously and returns the response text.
    """
    async with _groq_semaphore:
        try:
            completion = await groq_client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": _build_system_prompt()},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=450,
            )
     
            return completion.choices[0].message.content

        except Exception as e:
            print("GROQ async call error:", e)
            raise e

async def call_model(prompt: str, groq_client, model_name: str) -> str:
    """
    Public function to call the Groq LLM.
    """
    if groq_client is None:
        raise ValueError("Groq client not provided")
    return await _call_groq_async(groq_client, prompt, model_name)

async def medical_qa(query: str, groq_client, model_name: str) -> Tuple[str, List[str]]:
    """
    Retrieves context from knowledge base and asks Groq LLM.
    Returns (response_text, sources_list)
    """
    docs = retrieve_knowledge(query)
    context = "\n\n".join([d.get("text", "") for d in docs])
    sources = [d.get("source", "Unknown") for d in docs]

    prompt = f"""
Use the context to answer safely and concisely. If uncertain, advise to see a doctor.

Context: {context}

Question: {query}

Answer:
"""
    try:
        response_text = await call_model(prompt, groq_client, model_name)
        return response_text.strip(), sources
    except Exception as e:
        print("[Groq fallback] Error:", e)
        fallback = (
            "I could not access the language model right now. "
            "If this is urgent, please seek medical help."
        )
        return fallback, []

async def answer_medical_question(query: str, groq_client=None, model_name=None):
    """
    Entry point for FastAPI or other services.
    Automatically initializes AsyncGroq client if not provided.
    """
    model_name = model_name or CONFIG["MODEL_NAME"]

    if groq_client is None:
        if AsyncGroq:
            groq_client = AsyncGroq(api_key=CONFIG["GROQ_API_KEY"])
        else:
            raise ValueError("AsyncGroq SDK not installed or available.")

    return await medical_qa(query, groq_client, model_name)
