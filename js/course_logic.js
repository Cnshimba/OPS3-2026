// Course Logic: Progress Tracking & Quiz Guarding (LocalStorage Only)

// --- GLOBALS ---
let currentModuleId = window.location.pathname.split("/").pop().replace(".html", "").replace(".md", "");

// --- INITIALIZATION ---
document.addEventListener("DOMContentLoaded", () => {
    console.log("[Course Logic] Initializing (LocalStorage Mode)...");

    setupProgressBar();
    setupQuizGuard();
    loadLocalProgress();
});

// --- PROGRESS TRACKING ---
function setupProgressBar() {
    // Only for Student Notes/Articles
    const article = document.querySelector("article");
    if (!article) return;

    // Create Bar Container
    const barContainer = document.createElement("div");
    barContainer.className = "fixed top-16 left-0 w-full h-1 bg-gray-200 dark:bg-gray-700 z-40";

    const bar = document.createElement("div");
    bar.id = "read-progress";
    bar.className = "h-full bg-blue-600 dark:bg-sky-400 transition-all duration-150";
    bar.style.width = "0%";

    barContainer.appendChild(bar);
    document.body.appendChild(barContainer);

    // Scroll Listener
    window.addEventListener("scroll", () => {
        const scrollTop = window.scrollY;
        const docHeight = document.body.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;

        document.getElementById("read-progress").style.width = Math.min(100, scrollPercent) + "%";

        // Mark Complete if > 90%
        if (scrollPercent > 90) {
            markModuleComplete();
        }
    });
}

function loadLocalProgress() {
    if (localStorage.getItem("COMPLETED_" + currentModuleId)) {
        console.log("[Progress] Module already completed");
        unlockQuizButton();
    }
}

function markModuleComplete() {
    const isAlreadyComplete = localStorage.getItem("COMPLETED_" + currentModuleId);
    if (isAlreadyComplete) return;

    console.log("[Progress] Module Completed:", currentModuleId);
    localStorage.setItem("COMPLETED_" + currentModuleId, "true");

    // Unlock Quiz Immediately
    unlockQuizButton();
}

// --- QUIZ GUARD ---
function setupQuizGuard() {
    const btn = document.getElementById("start-quiz-btn");
    if (!btn) return;

    // Check if ALREADY unlocked
    const isComplete = localStorage.getItem("COMPLETED_" + currentModuleId);

    if (!isComplete) {
        lockQuizButton(btn);
    } else {
        unlockQuizButton();
    }
}

function lockQuizButton(btn) {
    btn.classList.add("opacity-50", "cursor-not-allowed", "grayscale");
    btn.dataset.locked = "true";
    btn.onclick = (e) => {
        if (btn.dataset.locked === "true") {
            e.preventDefault();
            alert("🔒 Quiz Locked!\n\nPlease read through the notes first.\n(Scroll to the bottom to unlock)");
            return false;
        }
    };
}

function unlockQuizButton() {
    const btn = document.getElementById("start-quiz-btn");
    if (!btn) return;

    btn.classList.remove("opacity-50", "cursor-not-allowed", "grayscale");
    btn.dataset.locked = "false";
    btn.onclick = null; // Remove blocker
}
