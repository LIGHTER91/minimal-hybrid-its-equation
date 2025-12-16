import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"  # ou qwen2.5:7b


def generate_exercise(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9
        }
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    print("LLM Response:", response.json()["response"])
    return response.json()["response"]
