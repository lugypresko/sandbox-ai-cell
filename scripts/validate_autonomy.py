import subprocess
from pathlib import Path

import yaml


def get_changed_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def load_contract():
    path = Path("governance/autonomy/execution_contract.yaml")
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def classify(files, contract):
    forbidden = contract["autonomous_scope"]["forbidden_changes"]
    allowed = contract["autonomous_scope"]["allowed_changes"]

    touches_forbidden = []
    touches_allowed = []

    for name in files:
        if any(name.startswith(p.replace("/**", "")) for p in forbidden):
            touches_forbidden.append(name)
        elif any(name.startswith(p.replace("/**", "")) for p in allowed):
            touches_allowed.append(name)

    if touches_forbidden:
        return "ESCALATE", touches_forbidden

    return "AUTO_EXECUTE", touches_allowed


def main():
    files = get_changed_files()
    contract = load_contract()

    state, details = classify(files, contract)

    print("=== AUTONOMY ADVISORY REPORT ===")
    print(f"Changed files: {files}")
    print(f"Decision: {state}")

    if details:
        print("Details:")
        for name in details:
            print(f" - {name}")

    print("NOTE: Advisory mode only. No action taken.")


if __name__ == "__main__":
    main()
