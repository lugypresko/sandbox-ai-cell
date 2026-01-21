# CODEX.md -- AI-CELL Execution Contract

This document defines how CODEX (or any AI coding agent) must operate
when contributing code to the AI-CELL repository.

This is not guidance.
This is an execution contract.

Violation of these rules is considered a defect.

---

## 0. Prime Directive

CODEX acts as an implementation agent, not as:
- an architect
- a product designer
- a decision-maker
- a prompt engineer

CODEX implements exactly what is defined in:
- CONTRACT.md
- DECISION_MODEL.md
- POLICY.md
- SYSTEM.md
- MONITORS.md

If ambiguity exists, STOP and ask for clarification.

---

## 1. Repository Structure (Non-Negotiable)

CODEX must preserve the following structure at a minimum:

/
|-- CODEX.md
|-- docker-compose.yml
|-- Dockerfile.sandbox
|-- Dockerfile.engine
|-- .pre-commit-config.yaml
|-- .github/
|   |-- workflows/
|       |-- markdown-hygiene.yml
|-- sandbox/
|   |-- CONTRACT.md
|   |-- DECISION_MODEL.md
|   |-- POLICY.md
|   |-- SYSTEM.md
|   |-- MONITORS.md
|-- src/
|-- tests/

CODEX must not:
- add new top-level directories
- relocate files
- introduce alternate structures

---

## 2. Docker Rules

Docker is used only to enforce sandbox boundaries.

### Principles
- app-service represents system reality
- otel-collector is the hard telemetry boundary
- ai-cell-engine is the regulator

### Forbidden
- Direct calls from ai-cell-engine to application services
- Shared state between containers
- Business logic inside Dockerfiles

### Allowed
- Environment variables
- Volume mounts for logs or artifacts
- Deterministic startup scripts

CODEX must not alter the topology in docker-compose.yml.

---

## 3. Deterministic State Machine (Critical)

### Rule of Authority
The AI does not decide state.
The code decides state.

### Requirements
- Explicit state transitions
- Deterministic logic only
- No randomization
- No time-based shortcuts
- No heuristic shortcuts

State transitions must:
- Follow DECISION_MODEL.md exactly
- Enforce allowed transition paths
- Require persistence for escalation and recovery

CODEX must not:
- infer state using AI output
- add hidden thresholds
- skip RECOVERY

---

## 4. Drift and Evidence Buffer

### Buffer
- Use collections.deque
- Fixed window size
- Deterministic ordering

### Drift Calculation
Drift must be computed explicitly from:
- magnitude
- velocity (slope)
- duration

Forbidden:
- Pandas
- Auto-resampling
- Implicit smoothing
- Statistical magic

Drift math must be readable, testable, and reviewable.

---

## 5. Pydantic Usage (Mandatory)

All core data structures must be defined using Pydantic v2.

Requirements:
- frozen equals true (immutability)
- strict validation
- no free-form dicts

Applies to:
- signals
- decisions
- decision context
- explanations

If validation fails, execution must halt.

---

## 6. LLM Usage (Explanation Only)

### Absolute Rule
LLMs explain decisions.
They do not influence them.

### Allowed Interface
explain(decision_context) -> Explanation

The LLM:
- does not know state machine internals
- does not know policies beyond references
- cannot trigger actions
- cannot retry with altered prompts

Forbidden:
- prompt experimentation
- retries with modified context
- AI-generated logic paths

LLM output must never affect:
- state
- drift
- policy validation
- decision type

---

## 7. FastAPI Ingest Layer

FastAPI is used as a thin boundary only.

Responsibilities:
- receive telemetry
- validate schema
- enqueue or forward data

Forbidden:
- decision logic
- state inference
- aggregation
- drift analysis

If logic appears in the ingest layer, it is a defect.

---

## 8. Testing Requirements

CODEX must add or maintain tests for:

Determinism:
- same input produces same state and same decision

State transitions:
- all allowed transitions
- all forbidden transitions

Policy enforcement:
- invalid decisions must fail

CODEX must not:
- weaken tests to pass
- disable tests
- mock around core logic

If tests fail, STOP.

---

## 9. Documentation Rules

All Markdown files must:
- be UTF-8 encoded
- use ASCII-safe punctuation only
- contain no control characters

CODEX must not:
- rewrite CONTRACT.md semantics
- rephrase governance documents
- introduce stylistic changes

Documentation changes require explicit approval.

---

## 10. Stop Conditions

CODEX must stop and request clarification if:
- documents conflict
- requirements are ambiguous
- behavior is not explicitly defined
- temptation arises to improve logic

Correct response:
STOP - clarification required.

---

## 11. Final Reminder

AI-CELL is not evaluated on cleverness.

It is evaluated on:
- restraint
- predictability
- auditability
- correctness under pressure

CODEX exists to preserve these properties.

Nothing else.
