from services.skill_stractor import llamar_modelo
from services.pdf_reader import extract_text_pdf
from services.evaluator import evaluate_candidate

print("Leyendo PDF...")

cv_text = extract_text_pdf("CV_Alejandro_Lillo.pdf")
cv_oferta = extract_text_pdf("Oferta_Desarrollador.pdf")


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

def extract_skills_from_cv(cv_text):
    prompt = build_prompt(cv_text)
    skills = llamar_modelo(prompt)
    return skills

def extract_skills_from_job_offer(cv_oferta):
    prompt = build_prompt(cv_oferta)
    skills = llamar_modelo(prompt)
    return skills

candidate_skills = extract_skills_from_cv(cv_text)
required_skills = extract_skills_from_job_offer(cv_oferta)

evaluation_result = evaluate_candidate(required_skills, candidate_skills)
print(evaluation_result)
