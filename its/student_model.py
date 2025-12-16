import json
from datetime import datetime


class StudentModel:
    def __init__(self, path: str):
        self.path = path
        with open(path, "r") as f:
            data = json.load(f)

        self.mastery = data["mastery"]
        self.common_errors = data["common_errors"]
        self.history = data["history"]

    def update_after_attempt(self, concept: str, success: bool, error_type: str | None):
        if success:
            self.mastery[concept] = min(1.0, self.mastery.get(concept, 0.0) + 0.1)
        else:
            self.mastery[concept] = max(0.0, self.mastery.get(concept, 0.0) - 0.1)
            if error_type and error_type not in self.common_errors:
                self.common_errors.append(error_type)

        self.history.append({
            "concept": concept,
            "success": success,
            "error": error_type,
            "timestamp": datetime.utcnow().isoformat()
        })

    def save(self):
        with open(self.path, "w") as f:
            json.dump({
                "mastery": self.mastery,
                "common_errors": self.common_errors,
                "history": self.history
            }, f, indent=2)
