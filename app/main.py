from fastapi import FastAPI,UploadFile, File
from app.services.evaluator import evaluate_candidate
from app.services.skill_stractor import llamar_modelo
from app.services.pdf_reader import extract_text_pdf
from app.models.candidate_db import Candidate
from app.models.offer_db import JobOffer
from app.db import engine, session,Base
from pydantic import BaseModel
import json

app = FastAPI()

Base.metadata.create_all(bind=engine)

class JobOfferRequest(BaseModel):
    offer_name: str
    description: str


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

app.post("/job_offer")
async def create_job_offer(offer: JobOfferRequest):
    required_skills = llamar_modelo(build_prompt(offer.description))
    db = session()
    job_offer = JobOffer(
        offer_name=offer.offer_name,
        description=offer.description,
        required_skills=json.dumps(required_skills)
    )
    db.add(job_offer)
    db.commit()
    db.refresh(job_offer)
    db.close()
    return {
        "id": job_offer.id,
        "offer_name": job_offer.offer_name,
        "description": job_offer.description,
        "required_skills": required_skills
    }

app.get("/job_offers")
def get_job_offers():
    db = session()
    job_offers = db.query(JobOffer).all()
    db.close()
    return job_offers

@app.post("apply_offer/{offer_id}")
async def apply_offer(offer_id: int, cv_file: UploadFile = File(...)):
    db = session()
    job_offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()

    if not job_offer:
        db.close()
        return {"error": "Job offer not found"}
    
    with open(cv_file.filename, "wb") as f:
        f.write(await cv_file.file.read())
    cv_text = extract_text_pdf(cv_file.filename)
    candidate_skills = llamar_modelo(build_prompt(cv_text))
    required_skills = json.loads(job_offer.required_skills)
    candidate_score = evaluate_candidate(required_skills, candidate_skills)
    candidate = Candidate(
        cv_name=cv_file.filename,
        offer_name=job_offer.offer_name,
        candidate_skills=json.dumps(candidate_skills),
        required_skills=json.dumps(required_skills),
        score=candidate_score["score"],
        decision=candidate_score["decision"]
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    db.close()
    return {
        "cv_name": candidate.cv_name,
        "offer_name": candidate.offer_name,
        "candidate_skills": candidate_skills,
        "required_skills": required_skills,
        "score": candidate.score,
        "decision": candidate.decision
    }

@app.get("/candidates")
def get_candidates():
   db = session()
   candidates = db.query(Candidate).all()
   db.close()
   return candidates
