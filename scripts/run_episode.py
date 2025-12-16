import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from its.domain_model import DomainModel
from its.student_model import StudentModel
from its.tutor_model import TutorModel

from generation.llm_generator import generate_exercise
from generation.prompt_templates import exercise_generation_prompt

from agents.verifier_agent import VerifierAgent
from evaluation.llm_judge import LLMJudge
from simulation.simulate_student import SimulatedStudent


def main():
    print("=== Running one ITS episode ===")

    # 1️ Load models
    domain = DomainModel("data/domain/pedagogical_graph.json")
    student = StudentModel("data/students/student_profile.json")
    tutor = TutorModel(domain)

    verifier = VerifierAgent(domain)
    judge = LLMJudge()
    simulated_student = SimulatedStudent(student)

    # 2️ Pedagogical decision
    decision = tutor.pedagogical_decision(student)

    concept = decision["concept"]
    difficulty = decision["difficulty"]
    target_errors = decision["target_errors"]

    concept_name = domain.get_concept_name(concept)

    print(f"\nSelected concept: {concept} ({concept_name})")
    print(f"Difficulty level: {difficulty}")
    print(f"Target errors: {target_errors}")

    # 3️ Generate exercise
    prompt = exercise_generation_prompt(
        concept=concept,
        concept_name=concept_name,
        difficulty=difficulty,
        target_errors=target_errors
    )

    raw_output = generate_exercise(prompt)

    # 4️Verify exercise
    is_valid, reasons, exercise = verifier.verify(
        raw_output=raw_output,
        expected_concept=concept
    )

    if not is_valid:
        print("\n❌ Exercise rejected by verifier")
        for r in reasons:
            print("-", r)
        return

    print("\n✅ Exercise accepted")
    print("Exercise:", exercise["exercise"])
    print("Proposed solution:", exercise["solution"]["final_answer"])

    # 5️ Simulate student attempt
    success, error_type = simulated_student.attempt_exercise(concept)

    print("\nStudent attempt:")
    print("Success:", success)
    if error_type:
        print("Error type:", error_type)

    # 6️ Update student model
    student.update_after_attempt(
        concept=concept,
        success=success,
        error_type=error_type
    )

    # 7️ Pedagogical evaluation (LLM-as-judge)
    evaluation = judge.evaluate(exercise)

    if "error" in evaluation:
        print("\n⚠️ Judge error:", evaluation["error"])
    else:
        print("\n📊 Pedagogical evaluation:")
        print("Overall score:", evaluation["overall_score"])
        print("Feedback:", evaluation["feedback"])

    # 8️ Save updated student model
    student.save()

    print("\n=== Episode completed ===")


if __name__ == "__main__":
    main()
