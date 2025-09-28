# NAPTELLIGENCE 🚀😴

![Logo.](/assets/Naptelligence.png)

## Project Description

NapTelligence is a simple AI-powered app that acts as your personal sleep coach. It connects to your wearable device (like a Fitbit) to track your sleep patterns, creates easy-to-follow daily tips to improve your rest, and sends gentle reminders to build better sleep habits. Built as an autonomous agent, it runs in the background to make better sleep feel effortless.

  ![Imagen1.](/assets/License-Apache-2.0-blue.svg)
  ![Imagen2.](/assets/Python-3.8+-blue.svg)

## What It Aims to Solve

Many people struggle with sleep issues like jet lag or insomnia, which zap their energy and hurt daily productivity. NapTelligence tackles this by turning raw sleep data into actionable, personalized nudges without overwhelming the user.
Goals

🔍 Track basic sleep patterns from your wearable to spot trends like short nights or restless sleep.

📝 Generate simple daily plans, such as "Aim for 7-8 hours tonight" or "Wind down 30 minutes early."

🔔 Send one quick reminder per day via push notification to encourage small habit changes.

## Tech Stack

### Backend
Python 3.11: The core programming language for the agent's logic.
FastAPI: A modern, high-performance web framework used to build the API for the agent.
Pydantic: Used within FastAPI for data validation and ensuring the input and output data match the required schemas.
Uvicorn: An ASGI server that runs the FastAPI application, making it accessible via HTTP.

### Artificial Intelligence
Google Generative AI (Gemini): The AI model (gemini-1.5-flash) that powers the agent's core logic, responsible for analyzing sleep data and generating insights.

### Frontend (for the Demo UI)
HTML5: The standard markup language for creating the web page structure.
CSS3: Used for styling the web interface, including the mobile phone mockups and overall layout.
JavaScript: Powers the interactivity of the demo page, handling file uploads, API requests to the agent, and displaying the results dynamically.

### Deployment
Docker: Used to containerize the application, ensuring it runs consistently across different environments.
Maestro: The configuration files suggest the agent is designed to be managed and deployed using the Maestro platform for autonomous agents

## Setup Instructions

### Step 1: Download the Code
First, clone the project repository to your local machine using Git, or simply download and unzip the project files.

Bash
git clone https://github.com/your-username/naptelligence-agent.git
cd naptelligence-agent

### Step 2: Get Your Google AI (Gemini) API Key
To use the agent, you need a Gemini API key.
Go to the Google AI Studio website.
Sign in with your Google account.
Click on "Get API key" in the top left menu.
Click "Create API key in new project".
Copy the generated API key. Keep it safe, as you'll need it in the next step.

### Step 3: Create the Secret Variable
The agent uses a Secret variable to manage your secret API key locally.
Update your agent by adding the variable with your API key in the manage agents area of the Maestro website.
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"

### Step 4: Install Dependencies
The project uses a requirements.txt file to manage its Python libraries. Install them using pip.
Bash
pip install -r requirements.txt

### Step 5: Run the Agent Locally
You can now start the agent on your local machine using the Uvicorn server, which is specified in the Dockerfile.
Bash
uvicorn main:app --host 0.0.0.0 --port 8080
Your agent is now running! You can open a web browser and navigate to http://localhost:8080/docs to see the automatically generated API documentation and test the endpoints.

### Step 6: Add the API Key to Agent Secrets for Deployment
When you are ready to deploy your agent (for example, using a platform like Maestro), you must add your Gemini API key as a secret.
Navigate to your agent's settings on your deployment platform.
Find the "Secrets" or "Environment Variables" section.
Create a new secret with the exact name 
GOOGLE_API_KEY.
Paste your Gemini API key into the value field.
Save and redeploy your agent.
This ensures your agent can securely access the Google AI services without exposing your key in the source code.

## Example API Calls
These are example requests and corresponding responses that show how to interact with the API.

**Endpoint:** `POST /analyze_sleep`
**URL:** `TU_URL_DE_SERVICIO/analyze_sleep`
**Header:** `Content-Type: application/json`


### Case 1: Ideal Sleep
This example demonstrates a request with an optimal sleep duration and few interruptions.

**Request:**
```json
{
  "date": "2025-09-28",
  "sleep_summary": {
    "start_time": "2025-09-27T22:05:00Z",
    "end_time": "2025-09-28T06:15:00Z",
    "total_duration_minutes": 430,
    "average_hr": 58,
    "average_hrv": 65,
    "interruptions_count": 3
  },
  "raw_data": [
    {
      "timestamp": "2025-09-27T23:30:00Z",
      "average_hr": 60,
      "average_hrv": 70,
      "status": "deep_sleep"
    },
    {
      "timestamp": "2025-09-28T02:10:00Z",
      "average_hr": 65,
      "average_hrv": 60,
      "status": "awake"
    }
  ]
}

**Output
```json
{
    "analysis_summary": "Great job on getting almost 8.25 hours of sleep last night! Your average heart rate during sleep was a healthy 60 bpm, and your HRV was a solid 70. You only experienced one interruption, which is fantastic.  Your body appears to be recovering well. Keep up the good work!",
    "personalized_tips": [
        "Maintain a consistent sleep schedule, even on weekends, to further regulate your body's natural sleep-wake cycle.",
        "Consider a relaxing pre-sleep routine, such as reading or taking a warm bath, to signal to your body that it's time to wind down.",
        "Ensure your bedroom is dark, quiet, and cool to optimize your sleep environment.",
        "Given your good HRV, continue engaging in activities that promote relaxation and stress reduction, such as yoga or meditation."
    ],
    "daily_notification": {
        "title": "Sleep Update: Excellent Rest!",
        "body": "You achieved almost 8.25 hours of sleep last night with a low interruption count. Review your personalized sleep tips for continuous improvement!"
    }
}

### Case 2: Insufficient Sleep
This example demonstrates a request with a short sleep duration and potential signs of stress or poor sleep quality.
```json
{
  "date": "2025-09-29",
  "sleep_summary": {
    "start_time": "2025-09-28T23:00:00Z",
    "end_time": "2025-09-29T03:00:00Z",
    "total_duration_minutes": 240,
    "average_hr": 75,
    "average_hrv": 40,
    "interruptions_count": 2
  },
  "raw_data": [
    {
      "timestamp": "2025-09-29T01:30:00Z",
      "average_hr": 78,
      "average_hrv": 45,
      "status": "awake"
    },
    {
      "timestamp": "2025-09-29T02:45:00Z",
      "average_hr": 74,
      "average_hrv": 38,
      "status": "light_sleep"
    }
  ]
}

**output
```json
{
    "analysis_summary": "Your sleep on September 29, 2025, totaled 4 hours. While this is shorter than the recommended 7-9 hours for adults, your average heart rate (75 bpm) and HRV (40 ms) provide some insights. The two interruptions suggest potential areas for improvement in your sleep environment or pre-sleep routine.",
    "personalized_tips": [
        "Aim for a consistent sleep schedule by going to bed and waking up around the same time each day, even on weekends.",
        "Create a relaxing bedtime routine, such as reading, taking a warm bath, or listening to calming music, to wind down before sleep.",
        "Optimize your sleep environment by ensuring your bedroom is dark, quiet, and cool.",
        "Since you experienced two interruptions, evaluate potential causes like noise, light, or discomfort. Consider using earplugs, a sleep mask, or adjusting your thermostat.",
        "Focus on improving your HRV, as a higher HRV generally indicates better overall health and resilience. Practices like mindfulness, meditation, and regular exercise can help. Talk with your doctor before starting new exercises.",
        "Avoid caffeine and alcohol before bed, as they can disrupt your sleep cycle and affect your heart rate and HRV.",
        "Consider using a sleep tracking app or device to monitor your sleep patterns and identify potential triggers for interruptions or poor sleep quality."
    ],
    "daily_notification": {
        "title": "Sleep Insights - September 29, 2025",
        "body": "Your sleep duration was 4 hours with 2 interruptions. Your average HR was 75 bpm and HRV was 40 ms. Review your personalized tips for ways to improve!"
    }
}
## License

Copyright 2025 Nathalia Chivatá, Daniel Bernal

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


Made with ❤️ for better sleep. Star us if you like it! 🌟
