// AI Chat Logic (Gemini API Integration)

// Globals
// ⚠️ SECURITY WARNING: Embedding your key here makes it visible to anyone who extracts this file.
// For a classroom setting, this is often acceptable, but restricted your key's usage in Google Cloud Console if possible.
const EMBEDDED_KEY = "__GEMINI_API_KEY__"; // 🟢 GITHUB ACTIONS WILL REPLACE THIS AUTOMATICALLY

let GEMINI_API_KEY = (EMBEDDED_KEY && EMBEDDED_KEY !== "__GEMINI_API_KEY__") ? EMBEDDED_KEY : (localStorage.getItem("GEMINI_API_KEY") || "");
let chatHistory = [];
const SYSTEM_PROMPT = `
You are the AI Tutor for the OPS3(Virtualization and Cloud Infrastructure) course.
Your Goal: Answer student questions accurately using ONLY the provided Course Context.
    Rules:
        1. Use a friendly, encouraging professional tone.
2. If the answer is found in the context, explain it clearly.
3. If the answer is NOT in the context, politely say: "I can only answer questions related to the OPS3 course notes."
4. Do NOT hallucinate information not present in the notes.
6. Keep answers concise unless a detailed explanation is requested.
`;

const MAX_RETRIES = 3;

// VUT Navy Blue Theme Icons (Flat SVGs)
const COLOR_PRIMARY = "#002F6E";
const ICONS = {
    settings: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="${COLOR_PRIMARY}" width="20" height="20" style="vertical-align: middle;"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58a.49.49 0 0 0 .12-.61l-1.92-3.32a.488.488 0 0 0-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54a.484.484 0 0 0-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58a.49.49 0 0 0-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.58 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg>`,
    wave: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="${COLOR_PRIMARY}" width="16" height="16" style="vertical-align: middle;"><path d="M16 6l-1-1-4 4-4-4-1 1 5 5 5-5z" transform="rotate(180 12 12)"/></svg>`, // Simple filler, actually lets use a real HAND or INFO
    info: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="${COLOR_PRIMARY}" width="16" height="16" style="vertical-align: text-bottom;"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>`,
    check: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="${COLOR_PRIMARY}" width="16" height="16" style="vertical-align: text-bottom;"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>`,
    error: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="${COLOR_PRIMARY}" width="16" height="16" style="vertical-align: text-bottom;"><path d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z"/></svg>`,
    wait: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="${COLOR_PRIMARY}" width="16" height="16" style="vertical-align: text-bottom;"><path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"/><path d="M12.5 7H11v6l5.25 3.15.75-1.23-4.5-2.67z"/></svg>`,
    alert: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="${COLOR_PRIMARY}" width="16" height="16" style="vertical-align: text-bottom;"><path d="M12 2L1 21h22L12 2zm1 17h-2v-2h2v2zm0-4h-2V8h2v7z"/></svg>`
};

// Initialize
document.addEventListener("DOMContentLoaded", () => {
    // Check if context is loaded
    if (typeof COURSE_CONTEXT === 'undefined') {
        console.error("COURSE_CONTEXT not loaded!");
        addMessage(`${ICONS.alert} Error: Course knowledge base not loaded.`, false);
        return;
    }

    setupUI();
});

function setupUI() {
    const header = document.querySelector('.chat-header');

    // Only show Settings Button if NO embedded key is present OR it's the placeholder
    if (!EMBEDDED_KEY || EMBEDDED_KEY === "__GEMINI_API_KEY__") {
        const settingsBtn = document.createElement('button');
        settingsBtn.innerHTML = ICONS.settings;
        settingsBtn.className = 'chat-settings-btn';
        settingsBtn.title = "Configure API Key";
        settingsBtn.onclick = (e) => {
            e.stopPropagation();
            toggleSettings();
        };
        header.appendChild(settingsBtn);

        // Initial Greeting for Setup
        if (!localStorage.getItem("GEMINI_API_KEY")) {
            addMessage(`${ICONS.info} Hi! To use the AI Tutor, please configure the API Key in settings.`, false);
        }
    } else {
        // Ready to go immediately
        console.log("AI Chat: Using Embedded Key");
    }
}

function toggleSettings() {
    let settingsDiv = document.getElementById('chatSettings');

    if (!settingsDiv) {
        // Create Settings UI if not exists
        settingsDiv = document.createElement('div');
        settingsDiv.id = 'chatSettings';
        settingsDiv.className = 'chat-settings-panel';
        settingsDiv.innerHTML = `
            <h4>${ICONS.settings} AI Settings</h4>
            <div class="input-group">
                <label>Google Gemini API Key:</label>
                <input type="password" id="apiKeyInput" placeholder="Paste your API Key here" value="${GEMINI_API_KEY}">
            </div>
            <p class="small-text">Key is stored locally in your browser. <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#c9984a">Get a Free Key</a></p>
            <button onclick="saveApiKey()">Save Key</button>
            <button class="close-btn" onclick="toggleSettings()">Close</button>
`;
        document.getElementById('chatContainer').appendChild(settingsDiv);
    }

    settingsDiv.classList.toggle('active');
}

function saveApiKey() {
    const input = document.getElementById('apiKeyInput');
    const newKey = input.value.trim();

    if (newKey) {
        localStorage.setItem("GEMINI_API_KEY", newKey);
        GEMINI_API_KEY = newKey;
        alert("API Key Saved!");
        toggleSettings();
        addMessage(`${ICONS.check} Key saved! Ask me anything about OPS3.`, false);
    }
}

// Global wrapper to start the message flow
window.sendMessage = async function () {
    const input = document.getElementById('chatInput');
    const question = input.value.trim();

    if (!question) return;

    // 1. Check API Key
    if (!GEMINI_API_KEY) {
        alert("Please set your Gemini API Key in Settings first!");
        toggleSettings();
        return;
    }

    // 2. Add User Message
    addMessage(question, true);
    input.value = '';

    // 3. Start recursive sending process
    await sendToGemini(question, 0);
};

// Recursive function to handle sending with retries
async function sendToGemini(question, retryCount = 0) {
    showTyping();

    // Simple "Full Context" approach: Text + Question
    const fullPrompt = `${SYSTEM_PROMPT} \n\nCOURSE CONTEXT: \n${COURSE_CONTEXT} \n\nSTUDENT QUESTION: ${question} `;

    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: [{
                    parts: [{ text: fullPrompt }]
                }]
            })
        });

        const data = await response.json();
        hideTyping();

        if (data.error) {
            console.error("Gemini Error:", data.error);

            // 429 / Quota Error Handling with Auto-Retry
            if ((data.error.code === 429 || data.error.message.includes('Quota')) && retryCount < MAX_RETRIES) {
                const waitTimeSeconds = (retryCount + 1) * 3; // 3s, 6s, 9s
                const waitTimeMs = waitTimeSeconds * 1000;

                addMessage(`${ICONS.wait} Rate limit hit. Auto-retrying in ${waitTimeSeconds}s... (Attempt ${retryCount + 1}/${MAX_RETRIES})`, false);

                setTimeout(() => {
                    sendToGemini(question, retryCount + 1);
                }, waitTimeMs);
                return; // Exit this execution, retry will trigger
            }

            if (data.error.code === 429) {
                addMessage(`${ICONS.error} <strong>Rate Limit Exceeded:</strong> Maximum retries reached. Please wait a minute before trying again.`, false);
            } else {
                addMessage(`${ICONS.error} API Error: ${data.error.message}`, false);
                diagnoseAvailableModels();
            }

        } else if (data.candidates && data.candidates[0].content) {
            const aiText = data.candidates[0].content.parts[0].text;
            addMessage(renderMarkdown(aiText), false);
        } else {
            addMessage(`${ICONS.error} Sorry, I couldn't generate a response. Try again.`, false);
        }

    } catch (error) {
        hideTyping();
        console.error("Fetch Error:", error);
        addMessage(`${ICONS.error} Connection Error: ${error.message}`, false);
        // We generally do NOT retry on hard connection errors unless specific codes
    }
}

async function diagnoseAvailableModels() {
    try {
        const listResp = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${GEMINI_API_KEY}`);
        const listData = await listResp.json();

        if (listData.models) {
            const modelNames = listData.models.map(m => m.name.replace('models/', '')).join(', ');
            addMessage(`${ICONS.info} <strong>Debug Info: Your Key supports:</strong> <span style="font-size:0.8em">${modelNames}</span>`, false);
        }
    } catch (e) {
        console.error("Could not list models:", e);
    }
}

// Simple Markdown Parser for responses
function renderMarkdown(text) {
    if (!text) return "";

    // Bold
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Headers
    text = text.replace(/^### (.*$)/gim, '<h4>$1</h4>');
    text = text.replace(/^## (.*$)/gim, '<h3>$1</h3>');

    // Lists
    text = text.replace(/^\* (.*$)/gim, '• $1');
    text = text.replace(/^- (.*$)/gim, '• $1');

    // Newlines to BR
    text = text.replace(/\n/g, '<br>');

    return text;
}

// --- UI Helpers (Moved from glossary.html) ---

let chatMinimized = false;

window.toggleChat = function () {
    const container = document.getElementById('chatContainer');
    const toggle = document.getElementById('chatToggle');
    chatMinimized = !chatMinimized;

    if (chatMinimized) {
        container.classList.add('minimized');
        toggle.textContent = '+';
    } else {
        container.classList.remove('minimized');
        toggle.textContent = '−';
    }
}

window.askQuestion = function (question) {
    const input = document.getElementById('chatInput');
    input.value = question;
    // Trigger resize or focus if needed
    input.focus();
    window.sendMessage();
}

function addMessage(text, isUser) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${isUser ? 'user' : 'bot'}`;
    messageDiv.innerHTML = text;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function showTyping() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.classList.add('active');
}

function hideTyping() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.classList.remove('active');
}
