// AI Chat Logic (Gemini API Integration)

// Globals
let GEMINI_API_KEY = localStorage.getItem("GEMINI_API_KEY") || "";
let chatHistory = [];
const SYSTEM_PROMPT = `
You are the AI Tutor for the OPS3 (Virtualization and Cloud Infrastructure) course.
Your Goal: Answer student questions accurately using ONLY the provided Course Context.
Rules:
1. Use a friendly, encouraging professional tone.
2. If the answer is found in the context, explain it clearly.
3. If the answer is NOT in the context, politely say: "I can only answer questions related to the OPS3 course notes."
4. Do NOT hallucinate information not present in the notes.
5. Format answers with Markdown (bold, lists, etc.) for readability.
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

    // Add Settings Button
    const settingsBtn = document.createElement('button');
    settingsBtn.innerHTML = '⚙️';
    settingsBtn.className = 'chat-settings-btn';
    settingsBtn.onclick = (e) => {
        e.stopPropagation();
        toggleSettings();
    };
    header.appendChild(settingsBtn);

    // Initial Greeting
    if (!localStorage.getItem("GEMINI_API_KEY")) {
        addMessage("👋 Hi! To use the AI Tutor, please click the ⚙️ icon above and add your Google Gemini API Key. It's free and private!", false);
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

    const fullPrompt = `${SYSTEM_PROMPT}\n\nCOURSE CONTEXT:\n${COURSE_CONTEXT}\n\nSTUDENT QUESTION: ${question}`;

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
            addMessage(`❌ API Error: ${data.error.message}`, false);
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
    }
};

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
