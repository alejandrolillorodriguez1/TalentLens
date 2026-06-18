from fastapi import FastAPI,UploadFile, File
from app.services.evaluator import evaluate_candidate
from app.services.skill_stractor import llamar_modelo
from app.services.pdf_reader import extract_text_pdf
from app.models.candidate_db import Candidate
from app.db import engine, session
import json

app = FastAPI()

Candidate.metadata.create_all(bind=engine)

def build_prompt(texto):
    return f"""
Eres un sistema de extracción de información para recursos humanos.

Extrae únicamente las habilidades técnicas de este texto.

Devuelve únicamente JSON válido.
No escribas explicaciones.
No uses markdown.
No uses frases introductorias.

Formato exacto:
{{
  "skills": [
    "Python",
    "Java",
    "SQL"
  ]
}}

Texto:
{texto}
"""

@app.post("/evaluate")
async def evaluate_candidate_endpoint(cv_text : UploadFile = File(...),cv_oferta: UploadFile = File(...)):
    with open(cv_text.filename, "wb") as f:
        f.write(await cv_text.read())
    with open(cv_oferta.filename, "wb") as f:
        f.write(await cv_oferta.read())

    cv_text = extract_text_pdf(cv_text.filename)
    cv_oferta = extract_text_pdf(cv_oferta.filename)

    promt_cv = build_prompt(cv_text)
    promt_oferta = build_prompt(cv_oferta)
    skills_cv = llamar_modelo(promt_cv)
    skills_oferta = llamar_modelo(promt_oferta)
    evaluation_result = evaluate_candidate(skills_oferta, skills_cv)

    db = session()
    candidate = Candidate(
        cv_name=cv_text.filename,
        offer_name=cv_oferta.filename,
        candidate_skills=json.dumps(skills_cv),
        required_skills=json.dumps(skills_oferta),
        score=evaluation_result["score"],
        decision=evaluation_result["decision"]
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    db.close()
    return {
        "candidate_id": candidate.id,
        "decision": evaluation_result["decision"],
        "score": evaluation_result["score"],
        "matched_skills": evaluation_result["matched_skills"],
        "missing_skills": evaluation_result["missing_skills"]
    }

