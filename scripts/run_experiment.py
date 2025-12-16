import argparse
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
from evaluation.metrics import Metrics
from simulation.simulate_student import SimulatedStudent


def run_experiment(episodes: int):
    print(f"=== Running ITS experiment ({episodes} episodes) ===")

    # Load core components
    domain = DomainModel("data/domain/pedagogical_graph.json")
    student = StudentModel("data/students/student_profile.json")
    tutor = TutorModel(domain)

    verifier = VerifierAgent(domain)
    judge = LLMJudge()
    simulated_student = SimulatedStudent(student)

    metrics = Metrics()

    for episode in range(1, episodes + 1):
        print(f"\n--- Episode {episode} ---")

        # 1️ Pedagogical decision
        decision = tutor.pedagogical_decision(student)
        concept = decision["concept"]
        difficulty = decision["difficulty"]
        target_errors = decision["target_errors"]

        concept_name = domain.get_concept_name(concept)

        # 2 Generate exercise
        prompt = exercise_generation_prompt(
            concept=concept,
            concept_name=concept_name,
            difficulty=difficulty,
            target_errors=target_errors
        )

        raw_output = generate_exercise(prompt)

        # 3️ Verify
        is_valid, reasons, exercise = verifier.verify(
            raw_output=raw_output,
            expected_concept=concept
        )

        if not is_valid:
            print("❌ Rejected:", reasons)
            metrics.log_reject()
            continue

        # 4️ Student attempt
        success, error_type = simulated_student.attempt_exercise(concept)

        student.update_after_attempt(
            concept=concept,
            success=success,
            error_type=error_type
        )

        # 5️ Pedagogical evaluation
        evaluation = judge.evaluate(exercise)

        if "error" in evaluation:
            print("⚠️ Judge error")
            metrics.log_reject()
            continue

        score = evaluation.get("overall_score", 0.0)
        metrics.log_accept(score)

        print(
            f"Accepted | Success={success} | "
            f"Score={score:.2f}"
        )

    # Save final student state
    student.save()

    # Print experiment summary
    print("\n=== Experiment summary ===")
    summary = metrics.summary()
    for k, v in summary.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run multiple ITS episodes and collect metrics."
    )
    parser.add_argument(
        "--episodes",
        type=int,
        default=20,
        help="Number of ITS episodes to run"
    )

    args = parser.parse_args()
    run_experiment(args.episodes)
