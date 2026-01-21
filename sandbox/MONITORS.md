# AI-CELL -- Monitoring the Monitor

## 1. Purpose

These monitors do not observe the system.
They observe AI-CELL itself.

Goal: ensure AI-CELL behaves as a disciplined regulator, not an impulsive agent.

## 2. Core Monitors

### Monitor 1 -- Decision Rate

Question: Is AI-CELL overreacting?

Tracks:
- Decisions per time window
- Decisions per state

Alert if:
- Decision rate spikes without state change

### Monitor 2 -- State Stability

Question: Are state transitions justified?

Tracks:
- Time spent per state
- Frequency of oscillation

Alert if:
- Rapid NORMAL to DEGRADED flipping

### Monitor 3 -- Drift Sensitivity

Question: Does AI-CELL detect the right things?

Tracks:
- Detected drifts
- Missed drifts
- False positives

Output:
- Precision / recall indicators

### Monitor 4 -- Policy Violations

Question: Did AI-CELL exceed authority?

Tracks:
- Decisions outside allowed level
- Missing policy references

Any violation = critical alert.

### Monitor 5 -- Explanation Quality

Question: Can decisions be audited?

Tracks:
- % decisions with full rationale
- Missing fields
- Ambiguous explanations

Incomplete explanations are treated as failures.

## 3. Review Cadence

- After each test run
- After each policy change
- Before any demo

## 4. Exit Criteria (Sandbox Validation)

The sandbox is considered valid when:
- States align with injected conditions
- Decisions are sparse and justified
- Monitors remain stable
- No silent failures occur

## Final Anchor (Shared Across All Docs)

AI-CELL is not here to look smart.
It is here to be predictable, auditable, and safe under pressure.
