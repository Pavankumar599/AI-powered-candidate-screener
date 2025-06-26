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


# Clone or unzip the repo
```bash
cd quasivo_screening_app
```

# Create a virtual environment (optional)
```bash
python -m venv .venv
```
```bash
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
```

# Install dependencies
```bash
pip install -r requirements.txt
```

# Paste your GEMINI_API_KEY in .env file


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
* Easily extensible to add authentication or DB storage later.

## License
MIT
