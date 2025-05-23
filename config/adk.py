from google.adk.agents import Agent
from datetime import datetime
from zoneinfo import ZoneInfo

def get_clinic_info(query: str) -> dict:
    if "mole removal" in query.lower():
        return {"status": "success", "report": "Prepare by avoiding makeup and fasting for 4 hours."}
    return {"status": "error", "error_message": "Information not available."}

def get_appointment_time(patient_id: str) -> dict:
    tz = ZoneInfo("Asia/Kolkata")
    now = datetime.now(tz)
    return {"status": "success", "report": f"Next appointment: {now.strftime('%Y-%m-%d %H:%M')} IST"}

def get_patient_agent():
    return Agent(
        name="derm_clinic_bot",
        model="gemini-2.0-flash",
        description="Handles patient queries for a dermatology clinic.",
        instruction="Answer patient queries accurately, ensuring compliance and no diagnosis.",
        tools=[get_clinic_info, get_appointment_time]
    )