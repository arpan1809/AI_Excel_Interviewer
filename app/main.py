from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os

from app.interview_flow import generate_first_question, generate_followup_question
from app.evaluator import evaluate_answers_batch
from app.report_generator import generate_report

app = FastAPI()
sessions = {}

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse(os.path.join("static", "index.html"))


@app.post("/start_interview")
async def start_interview(session_id: str = Form(...), candidate_name: str = Form(...)):
    first_q = generate_first_question()

    sessions[session_id] = {
        "candidate": candidate_name,
        "questions": [first_q],
        "answers": [],
        "total": 20,
    }

    return {
        "intro": f"👋 Hello {candidate_name}, I am your AI Excel Interviewer. "
                 f"I will ask you {sessions[session_id]['total']} questions. "
                 f"If you don't know an answer, leave it blank and we'll move on.",
        "first_question": first_q,
        "total": sessions[session_id]["total"],
    }

@app.post("/answer")
async def answer(session_id: str = Form(...), answer: str = Form("")):
    sess = sessions.get(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")

    sess["answers"].append(answer)

    if len(sess["answers"]) >= sess["total"]:
        # Done → evaluate all answers and save PDF
        evaluations = evaluate_answers_batch(sess["questions"], sess["answers"], batch_size=5)
        pdf_path = generate_report(sess["candidate"], sess["questions"], sess["answers"], evaluations)
        # Save path in session for later download
        sess["pdf_path"] = pdf_path

        
        return {"message": "Interview complete"}

    
    last_q = sess["questions"][-1]
    last_a = sess["answers"][-1]

    if last_a.strip() == "" or len(last_a.split()) < 3:
        difficulty = "easier"
    elif len(last_a.split()) > 20:
        difficulty = "harder"
    else:
        difficulty = "medium"

    next_q = generate_followup_question(last_q, last_a, difficulty, asked_so_far=sess["questions"])
    sess["questions"].append(next_q)

    return {
        "next_question": next_q,
        "progress": len(sess["answers"]) + 1,
    }



@app.post("/download_report")
async def download_report(session_id: str = Form(...)):
    sess = sessions.get(session_id)
    if not sess or "pdf_path" not in sess:
        raise HTTPException(status_code=404, detail="Report not found")

    pdf_path = sess["pdf_path"]
    return FileResponse(pdf_path, media_type="application/pdf", filename="Excel_Report.pdf")
