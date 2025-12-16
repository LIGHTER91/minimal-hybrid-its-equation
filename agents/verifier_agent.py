import json
from typing import Dict, Tuple, List
from its.domain_model import DomainModel


class VerifierAgent:
    """
    Agent responsible for verifying that a generated exercise
    complies with pedagogical and structural constraints.
    """

    def __init__(self, domain_model: DomainModel):
        self.domain_model = domain_model

    def verify(self, raw_output: str, expected_concept: str) -> Tuple[bool, List[str], Dict]:
        """
        Verify the LLM output.

        Returns:
            - is_valid (bool)
            - list of rejection reasons
            - parsed exercise (if valid, else empty dict)
        """

        reasons = []

        # 1️⃣ JSON parsing
        try:
            exercise = json.loads(raw_output)
        except json.JSONDecodeError:
            return False, ["Invalid JSON format"], {}

        # 2️⃣ Mandatory fields
        required_fields = ["concept", "difficulty", "exercise", "solution", "pedagogical_feedback"]
        for field in required_fields:
            if field not in exercise:
                reasons.append(f"Missing field: {field}")

        if reasons:
            return False, reasons, {}

        # 3️⃣ Concept compliance
        if exercise["concept"] != expected_concept:
            reasons.append(
                f"Concept mismatch: expected {expected_concept}, got {exercise['concept']}"
            )

        # 4️⃣ Solution structure
        solution = exercise.get("solution", {})
        if "steps" not in solution or "final_answer" not in solution:
            reasons.append("Solution must contain steps and final_answer")

        # 5️⃣ Basic mathematical sanity checks
        if not isinstance(solution.get("steps", []), list):
            reasons.append("Solution steps must be a list")

        if not isinstance(solution.get("final_answer", ""), str):
            reasons.append("Final answer must be a string")

        # 6️⃣ Pedagogical domain check
        allowed_errors = self.domain_model.get_common_errors(expected_concept)
        feedback = exercise.get("pedagogical_feedback", "").lower()

        for err in allowed_errors:
            # This is a soft check: not mandatory, but encouraged
            if err.replace("_", " ") in feedback:
                break

        # 7️⃣ Final decision
        is_valid = len(reasons) == 0

        return is_valid, reasons, exercise
