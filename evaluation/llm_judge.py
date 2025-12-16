import json
import requests
from typing import Dict

OLLAMA_URL = "http://localhost:11434/api/generate"
JUDGE_MODEL = "qwen2.5:3b"


class LLMJudge:
    def _build_prompt(self, exercise: Dict) -> str:
        return f"""
You are an expert mathematics education evaluator.

Evaluate the pedagogical quality of the following exercise.

Return STRICT JSON only.

{json.dumps(exercise, indent=2)}

Output format:
{{
  "pedagogical_clarity": int,
  "level_appropriateness": int,
  "mathematical_correctness": int,
  "overall_score": float,
  "feedback": "short feedback"
}}
"""

    def evaluate(self, exercise: Dict) -> Dict:
        payload = {
            "model": JUDGE_MODEL,
            "prompt": self._build_prompt(exercise),
            "stream": False,
            "options": {
                "temperature": 0.0
            }
        }

        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        raw = response.json()["response"]

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON from judge",
                "raw_output": raw
            }
