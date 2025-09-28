from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

# --- Definición de los modelos de datos (Input/Output) ---

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

# --- Inicialización de la aplicación FastAPI ---

app = FastAPI(
    title="NapTelligence Sleep Agent",
    description="An agent that analyzes sleep data to provide insights and tips.",
    version="1.0.0"
)

# --- Lógica del Agente ---

def analyze_sleep_data(data: SleepInput) -> SleepOutput:
    """
    Procesa los datos de sueño y genera un análisis, consejos y una notificación.
    """
    summary = data.sleep_summary
    duration = summary.total_duration_minutes
    interruptions = summary.interruptions_count

    analysis_summary = f"Análisis de sueño: Duración total de {duration} minutos con {interruptions} interrupciones."
    personalized_tips = []
    
    # Lógica de análisis y consejos
    if duration < 420: # Menos de 7 horas
        analysis_summary += " La duración del sueño fue corta."
        personalized_tips.append("Intenta acostarte 30 minutos antes para aumentar tu tiempo de sueño.")
    else:
        analysis_summary += " La duración del sueño fue adecuada."
        personalized_tips.append("¡Buen trabajo! Mantén una duración de sueño consistente.")

    if interruptions > 1:
        analysis_summary += " Se detectaron varias interrupciones."
        personalized_tips.append("Asegúrate de que tu habitación esté oscura, silenciosa y fresca para minimizar las interrupciones.")
    else:
        analysis_summary += " El sueño fue continuo."
        personalized_tips.append("Tu entorno de sueño parece ser efectivo para un descanso sin interrupciones.")

    # Creación de la notificación diaria
    notification = Notification(
        title="Tu Resumen de Sueño 😴",
        body=f"Dormiste {duration // 60}h {duration % 60}m con {interruptions} interrupciones. ¡Revisa tus consejos personalizados!"
    )
    
    return SleepOutput(
        analysis_summary=analysis_summary,
        personalized_tips=personalized_tips,
        daily_notification=notification
    )

# --- Endpoints de la API ---

@app.get("/", tags=["General"])
async def read_root() -> Dict[str, str]:
    return {"message": "Welcome to the NapTelligence API"}

@app.post("/analyze_sleep", response_model=SleepOutput, tags=["Sleep Analysis"])
async def analyze_sleep(sleep_data: SleepInput) -> SleepOutput:
    """
    Recibe los datos del sueño, los analiza y devuelve un resumen y consejos.
    """
    if sleep_data.sleep_summary.total_duration_minutes <= 0:
        raise HTTPException(status_code=400, detail="La duración del sueño debe ser mayor a cero.")
        
    return analyze_sleep_data(sleep_data)

@app.get("/health", tags=["General"])
async def health_check() -> Dict[str, str]:
    return {"status": "ok"}