import hashlib
from pathlib import Path


__version__ = "0.1.0"

MATRIX_PATH = Path("experiments/persona_factory_sandbox/persona_matrix.yaml")
SCRIPT_PATHS = [
    Path("experiments/persona_factory_sandbox/factory_hash.py"),
    Path("experiments/persona_factory_sandbox/generate_personas.py"),
    Path("experiments/persona_factory_sandbox/validate_personas.py"),
]


def _normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _read_text(path: Path) -> str:
    return _normalize_text(path.read_text(encoding="utf-8"))


def compute_factory_hash() -> str:
    if not MATRIX_PATH.exists():
        raise FileNotFoundError(f"matrix not found: {MATRIX_PATH}")

    payload = []
    payload.append(f"matrix:{MATRIX_PATH}\n")
    payload.append(_read_text(MATRIX_PATH))
    for path in SCRIPT_PATHS:
        payload.append(f"\ncode:{path}\n")
        payload.append(_read_text(path))

    blob = "".join(payload).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


if __name__ == "__main__":
    print(compute_factory_hash())
