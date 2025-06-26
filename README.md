# Quasivo AI Candidate Screening App

A lightweight Streamlit web application that uses Google's **Gemini 2.0‑Flash** model to automate first‑round candidate screening.

## Features
* **Local‑only runtime** – no cloud hosting required.
* Paste or upload **Job Description** text.
* Paste résumé text or **upload PDF** (auto‑parsed).
* Uses **Gemini API** to generate three tailored interview questions.
* Lets the candidate answer each question.
* Scores answers **1‑10** with Gemini.
* Persists every session (JD, résumé, Q&A, scores) as JSON in the local **`data/`** folder.

## Prerequisites
* Python 3.9+
* A Gemini API key with access to `gemini-2.0-flash`

## Setup

```bash
# Clone or unzip the repo
cd quasivo_screening_app

# Create a virtual environment (optional)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Store your key (NEVER commit!) 
echo "GEMINI_API_KEY=YOUR_KEY_HERE" > .env
```

## Run the App
```bash
streamlit run app.py
```

The app launches in your browser at `http://localhost:8501`.

## Folder Structure
```
quasivo_screening_app/
├── app.py
├── requirements.txt
├── README.md
├── .env            # your API key (not committed)
└── data/           # JSON session logs auto‑saved here
```

## Prompts
Example Gemini prompts used inside `app.py` are in the `generate_interview_questions` and `score_answer` functions.

## Bonus Ideas Implemented
* **PDF parsing** for résumé uploads via `PyPDF2`.
* Easily extensible to add authentication or DB storage later.

## License
MIT