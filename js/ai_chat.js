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

// Initialize
document.addEventListener("DOMContentLoaded", () => {
    // Check if context is loaded
    if (typeof COURSE_CONTEXT === 'undefined') {
        console.error("COURSE_CONTEXT not loaded!");
        addMessage("⚠️ Error: Course knowledge base not loaded.", false);
        return;
    }

    setupUI();
});

function setupUI() {
    const header = document.querySelector('.chat-header');

    // Only show Settings Button if NO embedded key is present OR it's the placeholder
    if (!EMBEDDED_KEY || EMBEDDED_KEY === "__GEMINI_API_KEY__") {
        const settingsBtn = document.createElement('button');
        settingsBtn.innerHTML = '⚙️';
        settingsBtn.className = 'chat-settings-btn';
        settingsBtn.title = "Configure API Key";
        settingsBtn.onclick = (e) => {
            e.stopPropagation();
            toggleSettings();
        };
        header.appendChild(settingsBtn);

        // Initial Greeting for Setup
        if (!localStorage.getItem("GEMINI_API_KEY")) {
            addMessage("👋 Hi! To use the AI Tutor, please configure the API Key in settings.", false);
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
            <h4>⚙️ AI Settings</h4>
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
        alert("✅ API Key Saved!");
        toggleSettings();
        addMessage("✅ Key saved! Ask me anything about OPS3.", false);
    }
}

// Override existing sendMessage from glossary.html (or replace logic there)
// We will simply attach this to the global scope to be called by HTML
window.sendMessage = async function () {
    const input = document.getElementById('chatInput');
    const question = input.value.trim();

    if (!question) return;

    // 1. Check API Key
    if (!GEMINI_API_KEY) {
        alert("Please set your Gemini API Key in Settings (⚙️) first!");
        toggleSettings();
        return;
    }

    // 2. Add User Message
    addMessage(question, true);
    input.value = '';
    showTyping();

    // 3. Build Payload
    // Simple "Full Context" approach: Text + Question
    // For 180k tokens, we send it all. Gemini 1.5 Flash handles 1M.

    const fullPrompt = `${SYSTEM_PROMPT} \n\nCOURSE CONTEXT: \n${COURSE_CONTEXT} \n\nSTUDENT QUESTION: ${question} `;

    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${GEMINI_API_KEY}`, {
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
            // Show immediate error
            addMessage(`❌ API Error: ${data.error.message}`, false);

            // Checking models in background
            diagnoseAvailableModels();
        } else if (data.candidates && data.candidates[0].content) {
            const aiText = data.candidates[0].content.parts[0].text;
            addMessage(renderMarkdown(aiText), false);
        } else {
            addMessage("❌ Sorry, I couldn't generate a response. Try again.", false);
        }

    } catch (error) {
        hideTyping();
        console.error("Fetch Error:", error);
        addMessage(`❌ Connection Error: ${error.message}`, false);
        diagnoseAvailableModels();
    }
};

async function diagnoseAvailableModels() {
    try {
        const listResp = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${GEMINI_API_KEY}`);
        const listData = await listResp.json();

        if (listData.models) {
            const modelNames = listData.models.map(m => m.name.replace('models/', '')).join(', ');
            addMessage(`ℹ️ <strong>Debug Info: Your Key supports:</strong> <span style="font-size:0.8em">${modelNames}</span>`, false);
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
