from services.skill_stractor import llamar_modelo
from services.pdf_reader import extract_text_pdf
from services.evaluator import evaluate_candidate

print("Leyendo PDF...")

cv_text = extract_text_pdf("CV_Alejandro_Lillo.pdf")

print("PDF leído")
print(f"Caracteres: {len(cv_text)}")

print("Enviando a Ollama...")

respuesta = llamar_modelo(f"""
Eres un sistema de extracción de información para recursos humanos.

Extrae TODAS las habilidades técnicas del siguiente CV.

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
CV:

{cv_text}
""")

candidate_skills = respuesta
required_skills = ["Python", "Azure", "Java"]
evaluation = evaluate_candidate(required_skills, candidate_skills)
print("Evaluación del candidato:" )
print(evaluation)
