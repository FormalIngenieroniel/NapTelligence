import maestro

# Definimos la clase de entrada que corresponde con el input_schema.json
# Esto permite a Maestro validar y estructurar los datos de entrada.
class SleepInput(maestro.Input):
    date: str
    sleep_summary: dict
    raw_data: list

# Definimos la interfaz del agente. En este caso, será una interfaz web.
class SleepAgentInterface(maestro.Interface):
    type: str = "web"
    input: maestro.Input = SleepInput

# Creamos la clase principal del agente "NapTelligence"
class NapTelligenceAgent(maestro.Agent):
    interfaces: list[maestro.Interface] = [SleepAgentInterface]
    
    def execute(self):
        # Cargamos los datos de entrada usando el SDK de Maestro.
        summary = maestro.load_input("sleep_summary")
        
        # --- Lógica de Análisis del Sueño ---
        # Aquí definimos las reglas para determinar la calidad del sueño.
        
        analysis_summary = ""
        personalized_tips = []
        notification_body = ""

        is_short_sleep = summary["total_duration_minutes"] < 420  # Menos de 7 horas
        is_restless_sleep = summary["interruptions_count"] > 3
        
        # Generar resumen y consejos basados en las reglas
        if is_short_sleep:
            analysis_summary = f"Anoche dormiste {summary['total_duration_minutes'] // 60} horas y {summary['total_duration_minutes'] % 60} minutos, un poco menos de lo recomendado."
            notification_body = "Tu sueño fue un poco corto anoche. ¡Intenta descansar un poco más esta noche! 😴"
            personalized_tips.append("Intenta acostarte 30 minutos antes para alcanzar las 7-8 horas de sueño recomendadas.")
        else:
            analysis_summary = f"¡Excelente! Anoche dormiste un total de {summary['total_duration_minutes'] // 60} horas y {summary['total_duration_minutes'] % 60} minutos."
            notification_body = "¡Tuviste una gran noche de descanso! Sigue así. ✨"
            
        if is_restless_sleep:
            analysis_summary += f" Notamos que tuviste {summary['interruptions_count']} interrupciones."
            personalized_tips.append("Para un sueño más profundo, considera crear un ambiente más oscuro y silencioso en tu habitación.")
            
        # Añadir un consejo general siempre
        personalized_tips.append("Mantén un horario de sueño y vigilia constante, incluso los fines de semana, para regular tu reloj biológico.")

        # Si no se activó ninguna regla negativa, damos un mensaje positivo
        if not is_short_sleep and not is_restless_sleep:
            personalized_tips.append("Tu patrón de sueño es muy saludable. ¡Continúa con esos buenos hábitos!")

        # --- Estructurar la Salida ---
        # Creamos el diccionario de salida que coincide con el output_schema.json
        return {
            "analysis_summary": analysis_summary,
            "personalized_tips": personalized_tips,
            "daily_notification": {
                "title": "Tu Resumen de Sueño 💤",
                "body": notification_body
            }
        }

# <-- CAMBIO CLAVE AQUÍ
# Desplegamos el agente y asignamos la aplicación FastAPI resultante a la variable 'app'.
# Uvicorn buscará esta variable 'app' para iniciar el servidor.
app = maestro.deploy(NapTelligenceAgent)