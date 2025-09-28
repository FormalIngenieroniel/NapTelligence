from fastapi import FastAPI, HTTPException
# 1. IMPORT THE CORS MIDDLEWARE
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

# --- Data Model Definition (Input/Output) ---

class SleepSummary(BaseModel):
    total_duration_minutes: int
    interruptions_count: int

class SleepInput(BaseModel):
    sleep_summary: SleepSummary

class Notification(BaseModel):
    title: str
    body: str

class SleepOutput(BaseModel):
    analysis_summary: str
    personalized_tips: List[str]
    daily_notification: Notification

# --- FastAPI Application Initialization ---

app = FastAPI(
    title="NapTelligence Sleep Agent",
    description="An agent that analyzes sleep data to provide insights and tips.",
    version="1.0.0"
)

# 2. DEFINE THE ALLOWED ORIGINS (WE USE "*" TO ALLOW ALL)
origins = ["*"]

# 3. ADD THE MIDDLEWARE TO YOUR APPLICATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Agent Logic ---

def analyze_sleep_data(data: SleepInput) -> SleepOutput:
    """
    Processes sleep data and generates an analysis, tips, and a notification.
    """
    summary = data.sleep_summary
    duration = summary.total_duration_minutes
    interruptions = summary.interruptions_count

    analysis_summary = f"Sleep Analysis: Total duration of {duration} minutes with {interruptions} interruptions."
    personalized_tips = []
    
    if duration < 420:
        analysis_summary += " Sleep duration was short."
        personalized_tips.append("Try to go to bed 30 minutes earlier to increase your sleep time.")
    else:
        analysis_summary += " Sleep duration was adequate."
        personalized_tips.append("Good job! Maintain a consistent sleep duration.")

    if interruptions > 1:
        analysis_summary += " Several interruptions were detected."
        personalized_tips.append("Make sure your room is dark, quiet, and cool to minimize interruptions.")
    else:
        analysis_summary += " Sleep was continuous."
        personalized_tips.append("Your sleep environment seems to be effective for an uninterrupted rest.")

    notification = Notification(
        title="Your Sleep Summary 😴",
        body=f"You slept for {duration // 60}h {duration % 60}m with {interruptions} interruptions. Check out your personalized tips!"
    )
    
    return SleepOutput(
        analysis_summary=analysis_summary,
        personalized_tips=personalized_tips,
        daily_notification=notification
    )

# --- API Endpoints ---

@app.get("/", tags=["General"])
async def read_root() -> Dict[str, str]:
    return {"message": "Welcome to the NapTelligence API"}

@app.post("/analyze_sleep", response_model=SleepOutput, tags=["Sleep Analysis"])
async def analyze_sleep(sleep_data: SleepInput) -> SleepOutput:
    if sleep_data.sleep_summary.total_duration_minutes <= 0:
        raise HTTPException(status_code=400, detail="Sleep duration must be greater than zero.")
        
    return analyze_sleep_data(sleep_data)

@app.get("/health", tags=["General"])
async def health_check() -> Dict[str, str]:
    return {"status": "ok"}