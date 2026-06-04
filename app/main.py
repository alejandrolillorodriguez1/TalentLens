from fastapi import FastAPI
from app.models.candidate import Candidate
from app.services.evaluator import evaluate_candidate

app = FastAPI()

@app.get("/")
async def root():
    return {
        "nombre" : "TalentLens",
        "estado" : "Corriendo"
    }

@app.post("/evaluate")
async def evaluate(request : Candidate):
    result = evaluate_candidate(request.skills)
    return {
        "name" : request.name,
        "result" : result
}

    