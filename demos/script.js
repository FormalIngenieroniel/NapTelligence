const fileInput = document.getElementById('fileInput');
const analyzeButton = document.getElementById('analyzeButton');
const errorMessage = document.getElementById('error-message');
const responseArea = document.getElementById('response-area');
const rawOutput = document.getElementById('rawOutput');

const phoneScreen1 = document.getElementById('phoneScreen1');
const phoneScreen2 = document.getElementById('phoneScreen2');

const apiUrl = 'https://maestro-7edfc02c-cfb3-4237-9095-1ee43f57ad25-zcaxlbuauq-uc.a.run.app/analyze_sleep';

analyzeButton.addEventListener('click', async () => {
    errorMessage.style.display = 'none';
    responseArea.style.display = 'none';
    phoneScreen1.style.display = 'none';
    phoneScreen2.style.display = 'none';

    if (fileInput.files.length === 0) {
        errorMessage.textContent = '❌ Please select a JSON file first.';
        errorMessage.style.display = 'block';
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.readAsText(file);

    reader.onload = async (event) => {
        let jsonData;
        try {
            jsonData = JSON.parse(event.target.result);
        } catch (error) {
            errorMessage.textContent = '❌ Error processing file. Make sure it is a valid JSON.';
            errorMessage.style.display = 'block';
            return;
        }

        analyzeButton.disabled = true;
        rawOutput.textContent = 'Analyzing... Please wait.';
        responseArea.style.display = 'block';

        phoneScreen1.innerHTML = '<p style="text-align: center; color: #606770;">Analyzing...</p>';
        phoneScreen2.innerHTML = '<p style="text-align: center; color: #606770;">Analyzing...</p>';
        phoneScreen1.style.display = 'flex';
        phoneScreen2.style.display = 'flex';

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(jsonData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`API Error: ${response.status} - ${errorData.detail || 'Unknown error'}`);
            }

            const resultData = await response.json();

            // Update the plain text response area
            let formattedOutput = '📊 Sleep Summary:\n';
            formattedOutput += `${resultData.analysis_summary}\n\n`;
            formattedOutput += '💡 Personalized Tips:\n';
            resultData.personalized_tips.forEach(tip => {
                formattedOutput += `• ${tip}\n`;
            });
            formattedOutput += '\n';
            formattedOutput += '🔔 Daily Notification:\n';
            formattedOutput += `Title: ${resultData.daily_notification.title}\n`;
            formattedOutput += `Body: ${resultData.daily_notification.body}`;
            
            rawOutput.textContent = formattedOutput;
            responseArea.style.display = 'block';

            // Update the mobile phone visualization
            let screen1Content = `<h3>📊 Sleep Summary</h3>`;
            screen1Content += `<p>${resultData.analysis_summary}</p>`;
            screen1Content += `<h3>💡 Tips</h3><ul>`;
            resultData.personalized_tips.forEach(tip => {
                screen1Content += `<li>${tip}</li>`;
            });
            screen1Content += `</ul>`;
            phoneScreen1.innerHTML = screen1Content;
            
            let screen2Content = `
                <div class="notification-box">
                    <div class="notification-logo">
                        <img src="../assets/Naptelligence.png" alt="Notification" class="notification-icon">
                    </div>
                    <div class="notification-text">
                        <h4>${resultData.daily_notification.title}</h4>
                        <p>${resultData.daily_notification.body}</p>
                    </div>
                </div>
            `;
            phoneScreen2.innerHTML = screen2Content;
            
        } catch (error) {
            errorMessage.textContent = `❌ There was a problem with the request: ${error.message}`;
            errorMessage.style.display = 'block';
            responseArea.style.display = 'none';
            phoneScreen1.style.display = 'none';
            phoneScreen2.style.display = 'none';
        } finally {
            analyzeButton.disabled = false;
        }
    };

    reader.onerror = () => {
        errorMessage.textContent = '❌ Error reading file.';
        errorMessage.style.display = 'block';
        responseArea.style.display = 'none';
    };
});