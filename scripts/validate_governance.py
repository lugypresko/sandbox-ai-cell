#!/usr/bin/env python3
import sys
from pathlib import Path

import yaml


GOV_DIR = Path("governance/behavior")
REQUIRED_VERSION = "1.2"


def fail(message: str) -> None:
    print(f"[GOVERNANCE VIOLATION] {message}")
    raise SystemExit(1)


def _load_yaml(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{path} is not valid UTF-8: {exc}")
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        fail(f"{path} must be a YAML mapping")
    return data


def main() -> int:
    if not GOV_DIR.exists():
        fail("governance/behavior directory missing")

    yamls = sorted(GOV_DIR.glob("*.yaml"))
    if not yamls:
        fail("no governance YAML files found")

    for path in yamls:
        data = _load_yaml(path)
        version = data.get("version")
        if version != REQUIRED_VERSION:
            fail(f"{path} version {version!r} != {REQUIRED_VERSION}")

    print(f"[OK] Behavioral Safety Contract version {REQUIRED_VERSION} validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
