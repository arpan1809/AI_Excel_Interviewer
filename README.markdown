# AI-Powered Excel Mock Interviewer

An AI-powered web application to help candidates practice Excel-related technical interviews. The system dynamically generates questions, evaluates answers in real-time, and produces a detailed PDF report with scores and feedback.

## 🚀 Features

- ✅ **Dynamic Excel Interview Questions**: Powered by the Groq API for realistic, varied questions.
- ✅ **Adaptive Difficulty**: Questions adjust based on candidate responses for personalized practice.
- ✅ **Real-Time Answer Evaluation**: Scores responses on a 0–10 scale with immediate feedback.
- ✅ **Constructive Feedback**: Detailed insights to help candidates improve their Excel skills.
- ✅ **Auto-Generated PDF Report**: Stored in `/reports` directory and downloadable by candidates.
- ✅ **Web-Based Frontend**: Seamless, user-friendly interface for an interactive interview experience.
- ✅ **Dockerized Deployment**: Ready for deployment on Render, Railway, or Fly.io.

## 🏗️ Project Structure

```
excel-interviewer/
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── evaluator.py         # Answer evaluation logic (Groq API)
│   ├── interview_flow.py    # Q&A generation flow
│   ├── report_generator.py  # PDF report creation
│   ├── static/              # Frontend JS, CSS
│   ├── templates/           # HTML templates
├── reports/                 # Generated reports (PDFs)
├── requirements.txt         # Python dependencies
├── Dockerfile               # Deployment container spec
└── README.md                # Project documentation
```

## ⚡ Quickstart

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/excel-interviewer.git
cd excel-interviewer
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Setup Environment Variables

Create a `.env` file in the project root with the following:

```
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### 4️⃣ Run Locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 🐳 Run with Docker

Build the Docker image:

```bash
docker build -t excel-interviewer .
```

Run the container:

```bash
docker run -p 8000:8000 excel-interviewer
```

App available at: [http://localhost:8000](http://localhost:8000)

## 📑 Sample Report

After completing the mock interview, a PDF report is generated with the following sections:

- **Candidate Info**: Name and session details.
- **Scores for Each Question**: Individual question scores (0–10).
- **Average Performance**: Overall score summary.
- **Detailed Feedback**: Constructive insights for improvement.

### Example Report

```
Excel Mock Interview Report
Candidate: John Doe
Topic: Excel Interview

Q1: What is the difference between SUM and AutoSum in Excel?
Answer: SUM is manual, AutoSum inserts SUM quickly.
Score: 8
Feedback: Correct, could mention AutoSum button location.
...
Average Score: 7.5 / 10
```

## 🌐 Deployment

The application is configured for deployment on the following platforms:

- **Render**
- **Railway**
- **Fly.io**

The provided `Dockerfile` ensures seamless cloud deployment. Configure environment variables (e.g., `GROQ_API_KEY`, `GROQ_MODEL`) in your hosting platform’s dashboard.

## 🔮 Future Enhancements

- **Multi-Topic Support**: Extend to other interview topics (e.g., SQL, Python, Data Science).
- **Recruiter Dashboard**: Enable comparisons of candidate performance across sessions.
- **AI-Powered Adaptive Difficulty**: Enhance question personalization using advanced AI techniques.

## 👨‍💻 Author

Developed by **Arpan Chatterjee**