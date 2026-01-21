class GovernanceViolation(RuntimeError):
    pass


class GovernanceStateAdapter:
    def observe(self, state: str) -> None:
        if state == "PRESSURE":
            raise GovernanceViolation("sustained pressure requires governance intervention")
