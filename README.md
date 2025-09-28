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

Peticiones y respuestas de ejemplo para que lo demas lo usen facil

## License

Copyright 2025 Nathalia Chivatá, Daniel Bernal

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


Made with ❤️ for better sleep. Star us if you like it! 🌟
