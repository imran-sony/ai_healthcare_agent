# 🏥 AI Healthcare Agent
This project is an AI-powered medical assistant that can:

✅ Answer medical questions using LLM + medical knowledge base (RAG)  
✅ Check symptoms & risk level  
✅ Detect medical emergencies  
✅ Schedule appointments  
✅ Maintain chat session memory  
✅ Run completely async using Groq API  
✅ Serve via FastAPI REST API  

## 🚀 Features  
Feature	Description  
Medical QA ->	LLM + RAG (trusted medical docs)  
Symptom Checker ->	Simple rule-based triage  
Emergency Detection	-> Alerts user if risk is high  
Appointment Scheduler	-> Simulated booking reply  
Chat History ->	Keeps last 20 interactions  
Async	-> Fast + scalable  

## 📁 Project Structure  
│── core/  
│   ├── agent.py  
│   ├── pipeline.py  
│── modules/  
│   ├── medical_qa.py  
│   ├── medical_rag.py  
│   ├── alert_monitor.py  
│   ├── symptom_checker.py  
│   ├── appointment_manager.py  
│── utils/  
│   ├── config.py  
│── retrieval/  
│   ├── search.py  
│── main.py  
│── requirements.txt  
│── README.md  

## ⚙️ Installation  
### 1️⃣ Clone Repository  
git clone https://github.com/imran-sony/ai_healthcare_agent.git  
cd ai_healthcare_agent  

### 2️⃣ Create Virtual Environment  
python -m venv venv  
venv\Scripts\activate  

### 3️⃣ Install Dependencies  

pip install -r requirements.txt  

## 🔑 Environment Variables  

Create a .env file in project root:  

GROQ_API_KEY=your_groq_api_key  
MODEL_NAME=llama-3.3-70b-versatile  
REDIS_URL=redis://localhost:6379/0  

## ▶️ Run API Server  

uvicorn main:app --reload --host 0.0.0.0 --port 8000
