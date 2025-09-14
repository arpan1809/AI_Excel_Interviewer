let sessionId = null,
    currentIndex = 0,
    total = 20;

const nameInput = document.getElementById("name");
const startBtn = document.getElementById("start-btn");
const introEl = document.getElementById("intro");
const qaArea = document.getElementById("qa-area");
const progress = document.getElementById("progress");
const progressFill = document.getElementById("progress-fill");

// Generate a unique session ID
function uid() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
}

// Start interview
startBtn.addEventListener("click", async () => {
    const candidateName = nameInput.value.trim() || "Candidate";
    sessionId = uid();

    const body = new URLSearchParams({ session_id: sessionId, candidate_name: candidateName });
    const res = await fetch("/start_interview", { method: "POST", body });
    const data = await res.json();

    introEl.textContent = data.intro;
    currentIndex = 0;
    total = data.total || 20;
    progress.hidden = false;
    setProgress();
    showQuestion(data.first_question);
    startBtn.style.display = "none";
});

// Update progress bar
function setProgress() {
    progressFill.style.width = Math.round((currentIndex / total) * 100) + "%";
}

// Show a question in the UI
function showQuestion(q) {
    qaArea.innerHTML = `
        <div class="qa-card">
            <h3>Q${currentIndex + 1} of ${total}</h3>
            <p>${q}</p>
            <textarea id="answer"></textarea>
            <button class="btn" onclick="submitAnswer()">Submit Answer</button>
        </div>`;
}

// Submit answer from textarea
async function submitAnswer() {
    const text = document.getElementById("answer").value;
    await postAnswer(text || "");
}

// Handle answer submission
async function postAnswer(answer) {
    const body = new URLSearchParams({ session_id: sessionId, answer });
    const res = await fetch("/answer", { method: "POST", body });
    const data = await res.json();

    // ✅ If interview is complete
    if (data.message && data.message.includes("Interview complete")) {
        qaArea.innerHTML = `
            <p class="thank-you">✅ Thank you for completing the interview!</p>
            <button class="btn" onclick="downloadReport()">📥 Download Your Report</button>
        `;
        progressFill.style.width = "100%";
        return;
    }

    // Otherwise continue the interview
    currentIndex = data.progress - 1;
    setProgress();
    if (data.next_question) {
        showQuestion(data.next_question);
    }
}

// Download report only when candidate clicks
async function downloadReport() {
    const body = new URLSearchParams({ session_id: sessionId });
    const res = await fetch("/download_report", { method: "POST", body });
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "Excel_Report.pdf";
    a.click();
    URL.revokeObjectURL(url);
}
