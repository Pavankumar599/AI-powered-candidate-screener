import streamlit as st
import os
import json
import uuid
import datetime
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Google Generative AI
import google.generativeai as genai

#####################
# Helper functions  #
#####################

def init_gemini():
    """Configure the Gemini client from the GEMINI_API_KEY env var."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Environment variable GEMINI_API_KEY not set.")
        st.stop()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")


def save_session(payload: dict, output_dir: Path):
    """Persist the end‑to‑end session (JD, CV, Q&A, scores) to JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = output_dir / f"{datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S')}_{uuid.uuid4().hex[:8]}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return filename


def parse_pdf(file) -> str:
    """Best‑effort parse of PDF résumé to raw text."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        st.warning(f"Could not parse PDF: {e}")
        return ""


def generate_interview_questions(model, jd: str, cv: str) -> List[str]:
    prompt = f"""You are an HR assistant. Given the following job description and candidate résumé, create exactly three job‑specific interview questions.

    Job description:
    ---
    {jd}
    ---
    Candidate résumé:
    ---
    {cv}
    ---
    Return the four questions as a numbered list."""
    response = model.generate_content(prompt)
    # Ensure we always get three lines
    questions = [q.strip(" \n-") for q in response.text.strip().split("\n") if q.strip()]
    if len(questions) <= 3:
        questions.extend(["(Placeholder)" for _ in range(3 - len(questions))])
    return questions[:4]


def score_answer(model, jd: str, cv: str, question: str, answer: str) -> int:
    prompt = f"""You are an AI interviewer.

    Job description:
    ---
    {jd}
    ---
    Candidate résumé:
    ---
    {cv}
    ---
    Interview question: {question}
    Candidate answer: {answer}

    Score the candidate's answer from 1 (very poor) to 10 (excellent). Reply with only the integer."""
    response = model.generate_content(prompt)
    try:
        return int(response.text.strip().split()[0])
    except Exception:
        return 0


########################
# Streamlit UI Layer   #
########################

st.set_page_config(page_title="Quasivo AI Candidate Screener", layout="centered")
st.title("Quasivo – AI‑Powered Candidate Screener")

st.sidebar.header("Input Data")
jd_input_method = st.sidebar.radio("Job Description source", ["Paste text", "Upload file"])
if jd_input_method == "Paste text":
    job_description = st.sidebar.text_area("Job Description", height=200)
else:
    jd_file = st.sidebar.file_uploader("Upload JD file", type=["txt", "pdf", "md", "doc", "docx"])
    job_description = ""
    if jd_file:
        job_description = jd_file.read().decode("utf-8", errors="ignore")

cv_input_method = st.sidebar.radio("Résumé source", ["Paste text", "Upload PDF"])
if cv_input_method == "Paste text":
    resume_text = st.sidebar.text_area("Candidate Résumé", height=250)
else:
    cv_file = st.sidebar.file_uploader("Upload résumé (PDF)", type=["pdf"])
    resume_text = ""
    if cv_file:
        resume_text = parse_pdf(cv_file)

st.sidebar.markdown("---")
if st.sidebar.button("Generate Questions", disabled=not (job_description and resume_text)):
    if not (job_description and resume_text):
        st.error("Please provide both the job description and résumé text.")
        st.stop()
    model = init_gemini()
    questions = generate_interview_questions(model, job_description, resume_text)
    st.session_state["questions"] = questions
    st.session_state["answers"] = ["" for _ in questions]
    st.success("Questions generated! Scroll down to answer them.")

if "questions" in st.session_state:
    st.header("Interview Questions")
    for idx, q in enumerate(st.session_state["questions"]):
        if idx != 0:
            st.markdown(f"{q}")
            st.session_state["answers"][idx] = st.text_area(f"Your answer to Q{idx}", value=st.session_state["answers"][idx], key=f"ans_{idx}")

    if st.button("Score my answers"):
        model = init_gemini()
        scores = [score_answer(model, job_description, resume_text, q, a) for q, a in zip(st.session_state["questions"], st.session_state["answers"])]

        st.subheader("Results")
        for idx, (q, a, s) in enumerate(zip(st.session_state["questions"], st.session_state["answers"], scores)):
            if idx != 0:
                st.write(f"{q}")
                st.write(f"Answer: {a}")
                st.write(f"Score: :blue[{s}/10]")
                st.markdown("---")

        # Persist session
        record = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "job_description": job_description,
            "resume": resume_text,
            "questions": st.session_state["questions"],
            "answers": st.session_state["answers"],
            "scores": scores,
        }
        saved_file = save_session(record, Path("data"))

        st.success(f"Session saved to {saved_file}")