import random
from typing import Dict, Tuple


class SimulatedStudent:
    """
    Simple simulated student for closing the ITS loop.
    The student success probability depends on mastery,
    and errors follow known misconceptions.
    """

    def __init__(self, student_model):
        self.student_model = student_model

    def attempt_exercise(self, concept: str) -> Tuple[bool, str | None]:
        """
        Simulate an attempt on an exercise targeting a given concept.

        Returns:
            - success (bool)
            - error_type (str or None)
        """

        mastery = self.student_model.mastery.get(concept, 0.0)

        # Probability of success increases with mastery
        success_probability = min(0.9, mastery + 0.2)

        success = random.random() < success_probability

        if success:
            return True, None

        # If failure, sample a common error
        if self.student_model.common_errors:
            error = random.choice(self.student_model.common_errors)
        else:
            error = "unknown_error"

        return False, error
