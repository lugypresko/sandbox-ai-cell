# Definition of Done: Autonomy Advisory Mode

Scope: This DoD applies only to Autonomy Advisory Mode.

Done means:
- The advisory script reads `governance/autonomy/execution_contract.yaml` without errors.
- The advisory script lists changed files using the CI diff range (`origin/main...HEAD`).
- The advisory script outputs a decision of `AUTO_EXECUTE` or `ESCALATE` based on the contract.
- The advisory script always exits with code 0 (advisory only).
- The CI job `autonomy-advisory` runs on push and pull_request with `fetch-depth: 0`.

Not included:
- No runtime enforcement.
- No auto-correction or auto-revert actions.
- No contract content enforcement beyond the advisory report.
