import requests

def llamar_modelo(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1:8b",
            "prompt": prompt,
            "stream": False
        })
    data = response.json()
    return data["response"]