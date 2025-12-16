# Minimal Hybrid Intelligent Tutoring System (ITS)

## Description

This repository contains an **academic prototype of a hybrid Intelligent Tutoring System (ITS)** for solving first-degree linear equations. The system combines **explicit pedagogical rules** (symbolic decision-making) with a **locally executed Large Language Model (LLM)** operating under strict constraints.

The goal is **not** to achieve industrial-level performance, but to emphasize **architectural clarity**, **reproducibility**, and a **controlled integration of LLMs** within a classical ITS framework.

---

## Features

* Pedagogical domain model with prerequisite graph
* Simple student model (mastery levels, recurring errors, learning history)
* Rule-based tutor model (concept and difficulty selection)
* LLM-based exercise generation under explicit constraints
* Verifier agent for automatic acceptance / rejection
* LLM-as-judge for approximate pedagogical evaluation
* Probabilistic simulated student
* Multi-episode experimentation with quantitative metrics

---

## Architecture

The system is structured around the following components:

* **Domain Model**: mathematical concepts, prerequisites, common errors
* **Student Model**: mastery estimation and error tracking
* **Tutor Model**: pedagogical policy implemented as deterministic rules
* **LLM Generator**: constrained generation of exercises and solutions
* **Verifier Agent**: structural and pedagogical validation of LLM outputs
* **LLM-as-Judge**: automatic evaluation of pedagogical quality
* **Simulated Student**: closes the ITS loop without real learner data
* **Metrics Module**: quantitative analysis of system behavior

Architecture and sequence diagrams are provided in the `diagram/` directory.

---

## Technical Choices

* **Language**: Python 3.11
* **LLM backend**: Ollama (local execution)
* **Default model**: `phi3:mini`
* **Target OS**: Linux
* **Hardware**: consumer-grade machine (< 4 GB RAM)

Lightweight models are deliberately used to prioritize robustness, interpretability, and reproducibility over raw model capacity.

---

## Project Structure

```
minimal-hybrid-its-equations/
├── data/
│   ├── domain/
│   └── students/
├── its/
├── generation/
├── agents/
├── evaluation/
├── simulation/
├── scripts/
├── requirements.txt
└── README.md
```

---

## Installation

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start Ollama:

```bash
ollama serve
```

---

## Usage

### Run a single ITS episode

```bash
python scripts/run_episode.py
```

### Run a multi-episode experiment

```bash
python scripts/run_experiment.py --episodes 50
```


---

## Results (example)

For an experiment of 50 episodes:

```
total_exercises: 50
accepted: 13
rejected: 37
acceptance_rate: 0.26
average_score: 3.7 / 10
```

These results reflect:

* a deliberately strict verification policy,
* the limitations of small LLMs under strong constraints,
* the value of architectures designed to handle imperfect generations.

---

## Limitations

* No real learner data (simulated student only)
* No learning or adaptation in the tutor model
* Intentionally limited mathematical scope
* Simplified pedagogical evaluation

These limitations are **explicit design choices**, consistent with a research-oriented prototype.

---
