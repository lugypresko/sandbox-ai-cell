# ADR: Milestone 1 Deterministic Core Baseline

Decision: Drift thresholds are named defaults in code, not inline literals. This keeps classification policy explicit and stable, avoids "tuning by accident," and makes future adjustments deliberate and reviewable.

Decision: Tests assert identical transition timing for identical input sequences, not just the final state. Timing is part of the behavioral contract; allowing earlier or later transitions would change system behavior even if the end state matches.

Decision: Docker is excluded from Milestone 1. The goal is to lock deterministic core behavior before any environment or orchestration concerns are introduced, so the baseline cannot be masked by runtime noise.
