
document.addEventListener('DOMContentLoaded', () => {
    const root = document.getElementById('quiz-root');
    if (!root) return;

    // Data injection point (will be populated by Python script)
    const quizData = window.QUIZ_DATA || { questions: [] };

    let currentQuestionIndex = 0;
    let score = 0;
    let userAnswers = new Array(quizData.questions.length).fill(null);
    let quizState = 'START'; // START, QUIZ, RESULTS

    // Render Function
    function render() {
        root.innerHTML = '';
        const container = document.createElement('div');
        container.className = 'max-w-3xl mx-auto bg-[var(--bg-card)] rounded-xl shadow-lg overflow-hidden border border-[var(--border-color)] transition-colors duration-300';

        if (quizState === 'START') {
            renderStartScreen(container);
        } else if (quizState === 'QUIZ') {
            renderQuestionScreen(container);
        } else if (quizState === 'RESULTS') {
            renderResultsScreen(container);
        }

        root.appendChild(container);
    }

    function renderStartScreen(container) {
        const content = `
            <div class="p-8 text-center">
                <div class="mb-6 inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                </div>
                <h2 class="text-3xl font-bold mb-4 text-[var(--text-headings)]">Ready to Test Your Knowledge?</h2>
                <p class="text-[var(--text-body)] mb-8 text-lg">This quiz contains <span class="font-bold text-blue-600 dark:text-blue-400">${quizData.questions.length} questions</span>. Take your time and choose the best answer for each.</p>
                <button id="start-btn" class="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg text-lg transition-colors shadow-md">
                    Start Quiz
                </button>
            </div>
        `;
        container.innerHTML = content;
        container.querySelector('#start-btn').addEventListener('click', () => {
            quizState = 'QUIZ';
            render();
        });
    }

    function renderQuestionScreen(container) {
        const question = quizData.questions[currentQuestionIndex];
        const progress = Math.round(((currentQuestionIndex) / quizData.questions.length) * 100);

        const content = `
            <div class="h-2 bg-slate-200 dark:bg-slate-700 w-full">
                <div class="h-2 bg-blue-600 transition-all duration-500 ease-out" style="width: ${progress}%"></div>
            </div>
            <div class="p-8">
                <div class="flex justify-between items-center mb-6">
                    <span class="text-sm font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">Question ${currentQuestionIndex + 1} of ${quizData.questions.length}</span>
                    <span class="text-sm text-slate-400 font-mono">${Math.round((currentQuestionIndex / quizData.questions.length) * 100)}% Complete</span>
                </div>
                
                <h3 class="text-2xl font-bold mb-8 text-[var(--text-headings)] leading-snug">${question.text}</h3>
                
                <div class="space-y-3">
                    ${question.options.map((opt, idx) => `
                        <button class="option-btn w-full text-left p-4 rounded-lg border border-[var(--border-color)] hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all duration-200 group relative overflow-hidden" data-idx="${idx}">
                            <div class="flex items-start">
                                <span class="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 group-hover:bg-blue-600 group-hover:text-white transition-colors text-sm font-bold mr-4 border border-[var(--border-color)] group-hover:border-blue-600">
                                    ${String.fromCharCode(65 + idx)}
                                </span>
                                <span class="text-lg text-[var(--text-body)] group-hover:text-[var(--text-headings)] transform transition-transform group-hover:translate-x-1 pt-0.5">${opt}</span>
                            </div>
                        </button>
                    `).join('')}
                </div>
            </div>
            <div class="bg-[var(--bg-note)] p-4 border-t border-[var(--border-color)] flex justify-between items-center">
                 <button id="prev-btn" class="text-slate-500 hover:text-[var(--text-headings)] font-medium px-4 py-2 rounded transiton-colors ${currentQuestionIndex === 0 ? 'invisible' : ''}">
                    ← Previous
                 </button>
                 <span class="text-xs text-slate-400">Select an option to proceed</span>
            </div>
        `;

        container.innerHTML = content;

        container.querySelectorAll('.option-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                // Select Option Logic
                const selectedIdx = parseInt(btn.dataset.idx); // 0, 1, 2, 3
                // Map index 0->A, 1->B etc.
                const answerChar = String.fromCharCode(65 + selectedIdx);

                userAnswers[currentQuestionIndex] = answerChar;

                if (currentQuestionIndex < quizData.questions.length - 1) {
                    currentQuestionIndex++;
                    render();
                } else {
                    calculateScore();
                    quizState = 'RESULTS';
                    render();
                }
            });
        });

        container.querySelector('#prev-btn').addEventListener('click', () => {
            if (currentQuestionIndex > 0) {
                currentQuestionIndex--;
                render();
            }
        });
    }

    function calculateScore() {
        score = 0;
        quizData.questions.forEach((q, idx) => {
            if (userAnswers[idx] === q.correct) {
                score++;
            }
        });
    }

    function renderResultsScreen(container) {
        const percentage = Math.round((score / quizData.questions.length) * 100);
        let message = '';
        let colorClass = '';

        if (percentage >= 80) {
            message = 'Outstanding! You have mastered this module.';
            colorClass = 'text-green-600 dark:text-green-400';
        } else if (percentage >= 60) {
            message = 'Great job! You have a solid understanding.';
            colorClass = 'text-blue-600 dark:text-blue-400';
        } else {
            message = 'Keep It Up! Review the notes and try again.';
            colorClass = 'text-yellow-600 dark:text-yellow-400';
        }

        const content = `
            <div class="p-8 text-center">
                <div class="mb-2 text-sm font-semibold uppercase tracking-wider text-slate-500">Quiz Completed</div>
                <h2 class="text-4xl font-bold mb-4 ${colorClass}">
                    ${percentage}% Score
                </h2>
                <p class="text-xl text-[var(--text-headings)] mb-2 font-medium">You got ${score} out of ${quizData.questions.length} correct.</p>
                <p class="text-[var(--text-body)] mb-8">${message}</p>

                <div class="space-y-6 text-left mb-8">
                    <h3 class="text-lg font-bold border-b border-[var(--border-color)] pb-2 text-[var(--text-headings)]">Review Answers</h3>
                    ${quizData.questions.map((q, idx) => {
            const isCorrect = userAnswers[idx] === q.correct;
            const userAnsIdx = userAnswers[idx] ? userAnswers[idx].charCodeAt(0) - 65 : -1;
            const correctAnsIdx = q.correct.charCodeAt(0) - 65;

            return `
                        <div class="rounded-lg bg-[var(--bg-note)] p-4 border-l-4 ${isCorrect ? 'border-green-500' : 'border-red-500'}">
                            <p class="font-bold text-[var(--text-headings)] mb-2"><span class="text-slate-400 mr-2">Q${idx + 1}.</span> ${q.text}</p>
                            
                            <div class="text-sm space-y-1">
                                <div class="flex items-center ${isCorrect ? 'text-green-600 dark:text-green-400 font-bold' : 'text-red-500 line-through opacity-75'}">
                                    <span class="w-20 font-semibold text-slate-500 dark:text-slate-400">Your Ans:</span>
                                    <span>${userAnswers[idx] || 'Skipped'} (${userAnsIdx >= 0 ? q.options[userAnsIdx] : '-'})</span>
                                </div>
                                ${!isCorrect ? `
                                <div class="flex items-center text-green-600 dark:text-green-400 font-bold">
                                    <span class="w-20 font-semibold text-slate-500 dark:text-slate-400">Correct:</span>
                                    <span>${q.correct} (${q.options[correctAnsIdx]})</span>
                                </div>
                                ` : ''}
                            </div>
                        </div>
                        `
        }).join('')}
                </div>

                <div class="flex justify-center space-x-4">
                    <button id="retry-btn" class="px-6 py-2 bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 text-[var(--text-headings)] font-semibold rounded-lg transition-colors">
                        Retry Quiz
                    </button>
                    <a href="${quizData.courseIndexUrl || '../Course_Index.html'}" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors no-underline">
                        Back to Course
                    </a>
                </div>
            </div>
        `;
        container.innerHTML = content;

        container.querySelector('#retry-btn').addEventListener('click', () => {
            currentQuestionIndex = 0;
            score = 0;
            userAnswers = new Array(quizData.questions.length).fill(null);
            quizState = 'START';
            render();
        });
    }

    // Init
    render();
});
