import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import google.generativeai as genai

# --- Definición de los modelos de datos (Input/Output) ---
# Modelos actualizados para coincidir con input_schema.json

class SleepSummary(BaseModel):
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    total_duration_minutes: int
    average_hr: Optional[int] = None
    average_hrv: Optional[int] = None
    interruptions_count: int

class RawDataItem(BaseModel):
    timestamp: str
    average_hr: Optional[int] = None
    average_hrv: Optional[int] = None
    status: Optional[str] = None

class SleepInput(BaseModel):
    date: str
    sleep_summary: SleepSummary
    raw_data: List[RawDataItem]

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
# --- Configuración del cliente de Google AI ---
# La clave API se lee de la variable de entorno inyectada por Maestro
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Lógica del Agente con IA ---

def analyze_sleep_data_with_ai(data: SleepInput) -> SleepOutput:
    """
    Procesa los datos de sueño usando un modelo de IA para generar análisis.
    """
    # Convertir los datos de entrada a un string JSON para el prompt
    input_data_str = data.model_dump_json(indent=2)
    
    # --- CAMBIO AQUÍ ---
    # Modelo generativo de Google AI (nombre corregido)
    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = f"""
    Eres 'NapTelligence', un asistente experto en análisis del sueño. Tu objetivo es analizar los datos de sueño proporcionados en formato JSON y generar un resumen, consejos personalizados y una notificación.
    Tu respuesta DEBE ser un objeto JSON válido con la siguiente estructura:
    {{
      "analysis_summary": "string",
      "personalized_tips": ["string"],
      "daily_notification": {{
        "title": "string",
        "body": "string"
      }}
    }}
    Analiza la duración total, las interrupciones, y si están disponibles, el ritmo cardíaco (HR) y la variabilidad del ritmo cardíaco (HRV). Proporciona consejos prácticos y accionables. El tono debe ser de apoyo y motivador.

    Analiza los siguientes datos de sueño: {input_data_str}
    """

    try:
        response = model.generate_content(prompt)
                
        # Extraer y parsear el contenido JSON de la respuesta
        # La API de Gemini puede devolver el JSON con saltos de línea y ```json ```, lo limpiamos
        cleaned_json = response.text.replace("```json", "").replace("```", "").strip()
        ai_response_json = json.loads(cleaned_json)
        
        # Validar la respuesta con el modelo Pydantic
        return SleepOutput(**ai_response_json)

    except Exception as e:
        # En caso de error con la API de IA, se lanza una excepción HTTP
        raise HTTPException(status_code=500, detail=f"Error al procesar con IA: {e}")


# --- Endpoints de la API ---

@app.get("/", tags=["General"])
async def read_root() -> Dict[str, str]:
    return {"message": "Welcome to the NapTelligence API"}

@app.post("/analyze_sleep", response_model=SleepOutput, tags=["Sleep Analysis"])
async def analyze_sleep(sleep_data: SleepInput) -> SleepOutput:
    """
    Recibe los datos del sueño, los analiza con IA y devuelve un resumen y consejos.
    """
    if sleep_data.sleep_summary.total_duration_minutes <= 0:
        raise HTTPException(status_code=400, detail="La duración del sueño debe ser mayor a cero.")
        
    return analyze_sleep_data_with_ai(sleep_data)

@app.get("/health", tags=["General"])
async def health_check() -> Dict[str, str]:
    return {"status": "ok"}
