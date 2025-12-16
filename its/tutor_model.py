from typing import Dict, List
from its.domain_model import DomainModel
from its.student_model import StudentModel


class TutorModel:
    """
    Rule-based pedagogical tutor.
    Decides which concept and difficulty level to propose next
    based on the student model and the pedagogical graph.
    """

    def __init__(self, domain_model: DomainModel):
        self.domain_model = domain_model

    def select_next_concept(self, student: StudentModel) -> str:
        """
        Select the next pedagogical concept based on mastery and prerequisites.
        """

        # 1. Get all concepts whose prerequisites are satisfied
        available_concepts = self.domain_model.get_available_concepts(
            student.mastery
        )

        # 2. Prioritize low-mastery concepts
        available_concepts.sort(
            key=lambda c: student.mastery.get(c, 0.0)
        )

        return available_concepts[0]

    def select_difficulty(self, mastery: float) -> int:
        """
        Select difficulty level based on mastery.
        """
        if mastery < 0.4:
            return 1  # very simple
        elif mastery < 0.7:
            return 2  # standard
        else:
            return 3  # more challenging

    def pedagogical_decision(self, student: StudentModel) -> Dict:
        """
        Main pedagogical decision function.
        """

        concept = self.select_next_concept(student)
        mastery = student.mastery.get(concept, 0.0)
        difficulty = self.select_difficulty(mastery)

        target_errors: List[str] = []

        # If the student has recurring errors, target them explicitly
        for err in student.common_errors:
            if err in self.domain_model.get_common_errors(concept):
                target_errors.append(err)

        return {
            "concept": concept,
            "difficulty": difficulty,
            "target_errors": target_errors
        }
