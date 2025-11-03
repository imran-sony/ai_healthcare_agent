# main.py
# pip install fastapi uvicorn groq python-dotenv pydantic aiohttp redis sentence-transformers faiss-cpu
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.agent import HealthcareAgent
from utils.config import CONFIG

load_dotenv()

DEBUG = CONFIG.get("DEBUG", False)

app = FastAPI(title="AI Healthcare Agent")

agent = HealthcareAgent()

class UserQuery(BaseModel):
    session_id: str
    text: str


@app.post("/query")
async def query_agent(query: UserQuery):
    if not query.text or not query.session_id:
        raise HTTPException(status_code=400, detail="Missing session_id or text")

    try:
        response = await agent.run(query.text, query.session_id)
        return response
    except Exception as e:
        if DEBUG:
            raise HTTPException(status_code=500, detail=str(e))
        raise HTTPException(status_code=502, detail="Upstream LLM call failed")


@app.get("/")
def root():
    return {"message": "AI Healthcare Agent API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
