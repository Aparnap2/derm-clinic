from datetime import datetime
from zoneinfo import ZoneInfo
from config.ai_config import get_ai_client
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage

def get_clinic_info(query: str) -> Dict[str, Any]:
    if "mole removal" in query.lower():
        return {"status": "success", "report": "Prepare by avoiding makeup and fasting for 4 hours."}
    return {"status": "error", "error_message": "Information not available."}

def get_appointment_time(patient_id: str) -> Dict[str, Any]:
    tz = ZoneInfo("Asia/Kolkata")
    now = datetime.now(tz)
    return {"status": "success", "report": f"Next appointment: {now.strftime('%Y-%m-%d %H:%M')} IST"}

def get_patient_agent():
    llm = get_ai_client()
    
    def run_agent(query: str) -> str:
        messages = [
            SystemMessage(content="You are a helpful dermatology clinic assistant. Answer patient queries accurately and professionally. If you don't know the answer, say you'll find out and ask them to contact the clinic directly."),
            HumanMessage(content=query)
        ]
        response = llm.invoke(messages)
        return response.content
    
    return run_agent
