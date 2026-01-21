# AI-CELL -- Deterministic Decision Model

## 1. Purpose

This document defines how decisions are formed inside AI-CELL.

It is not code.
It is the decision grammar that all agents must follow.

Goal:
- Predictable behavior
- Auditable logic
- Clear separation between observation, interpretation, and action

## 2. Decision Pipeline (Non-negotiable Order)

Every decision MUST follow this exact sequence:
1. Signal Observation
2. Baseline Comparison
3. Drift Evaluation
4. State Inference
5. Policy Check
6. Decision Formation
7. Outcome Tracking

Skipping a step invalidates the decision.

## 3. Step Definitions

### 3.1 Signal Observation

Input:
- Metrics
- Logs
- Traces

Rules:
- Signals are raw
- No aggregation logic here
- No assumptions allowed

### 3.2 Baseline Comparison

Question:
"Is this within expected behavior?"

Baseline properties:
- Time-bound
- Scope-bound (service / dependency)
- Probabilistic, not absolute

Output:
- within_range
- out_of_range (magnitude, duration)

### 3.3 Drift Evaluation

Question:
"Is deviation meaningful or noise?"

Drift is defined by:
- Magnitude
- Duration
- Direction
- Velocity (rate of change)

Output:
- NO_DRIFT
- SOFT_DRIFT
- HARD_DRIFT

### 3.4 State Inference

State is inferred, not detected.

Allowed states:
- NORMAL
- DEGRADED
- PRESSURE
- RECOVERY

Rules:
- State change requires persistence
- State cannot skip levels
- RECOVERY is time-bound

### 3.5 Policy Check

Every potential decision is validated against:
- Authority level
- Blast radius
- Confidence threshold

If policy fails -- decision aborted.

### 3.6 Decision Formation

Decision types:
- NONE
- RECOMMEND
- ACT

Every decision must include:
- Triggering signals
- State
- Policy clause
- Confidence
- Expected effect

### 3.7 Outcome Tracking

Post-decision evaluation:
- Did state improve?
- Was drift reduced?
- Was decision unnecessary?

Outcome is logged and fed into future confidence weighting.

## 4. Determinism Principle

Given:
- Same signals
- Same baseline
- Same policy

AI-CELL must reach:
- The same decision.

If not -- bug.
