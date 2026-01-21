# Release Notes

## Baseline Milestones (v0.1)

This release captures the five milestone baselines with explicit tags.

Milestone 1 -- Deterministic Core
- Evidence buffer with deterministic ordering
- Drift math (magnitude, velocity, duration) and thresholds as named defaults
- Deterministic state machine with persistence guards
- Tests cover determinism and transition timing
- Tag: milestone-1-deterministic-core

Milestone 2 -- Decision Formation + Policy Gate
- Decision type is explicit and non-inferential
- Policy validates allow/block only; ACT blocked by default
- Tests assert deterministic decisions for same inputs
- Tag: milestone-2-decision-policy

Milestone 3 -- LLM as Narrator (Read-only)
- explain(decision_context) -> Explanation adapter only
- No feedback into state, drift, policy, or decision
- Tests prove explanation text does not alter decisions
- Tag: milestone-3-llm-narrator

Milestone 4 -- Docker Sandbox Integrity
- docker-compose sanity with app, dependency, otel, ai-cell engine
- Minimal sandbox services for latency injection
- OTel collector config and artifact logging mount
- Tag: milestone-4-docker-sandbox

Milestone 5 -- Hygiene and Enforcement
- Markdown hygiene check for UTF-8 and ASCII-safe punctuation
- Deterministic tests gated in CI
- Tag: milestone-5-hygiene-enforcement

Tests run locally:
- python -m pytest -p no:cacheprovider
