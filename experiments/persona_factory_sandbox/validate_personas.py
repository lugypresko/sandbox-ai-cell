import hashlib
import json
from pathlib import Path

import yaml

from factory_hash import __version__ as factory_hash_version
from factory_hash import compute_factory_hash


__version__ = "0.1.0"

ROOT = Path("experiments/persona_factory_sandbox")
MATRIX_PATH = ROOT / "persona_matrix.yaml"
OUTPUT_DIR = ROOT / "outputs"

PERSONAS_PATH = OUTPUT_DIR / "personas_v1_100.json"
DISTRIBUTION_PATH = OUTPUT_DIR / "distribution_report.json"
RUN_METADATA_PATH = OUTPUT_DIR / "run_metadata.json"
VALIDATION_PATH = OUTPUT_DIR / "validation_report.json"


def _load_matrix_version() -> str:
    if not MATRIX_PATH.exists():
        raise FileNotFoundError(f"matrix not found: {MATRIX_PATH}")
    with open(MATRIX_PATH, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict) or "version" not in data:
        raise ValueError("matrix missing version")
    return str(data["version"])


def _check_matrix_version() -> bool:
    try:
        return _load_matrix_version() == "0.1"
    except Exception:
        return False


def _read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _hash_file(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def _write_json(path: Path, payload: object) -> None:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    path.write_text(text, encoding="utf-8")


def _constraint(name: str, ok: bool, detail: str | None = None) -> dict:
    return {"name": name, "status": "pass" if ok else "fail", "detail": detail}


def _check_persona_dimensions() -> bool:
    if not PERSONAS_PATH.exists() or not MATRIX_PATH.exists():
        return False
    personas = _read_json(PERSONAS_PATH)
    with open(MATRIX_PATH, "r", encoding="utf-8") as handle:
        matrix = yaml.safe_load(handle)
    if not isinstance(personas, list) or not isinstance(matrix, dict):
        return False
    dims = matrix.get("dimensions", {})
    required = set(dims.keys())
    for item in personas:
        if not required.issubset(item.keys()):
            return False
    return True


def _check_empty_segments() -> bool:
    if not PERSONAS_PATH.exists() or not MATRIX_PATH.exists():
        return False
    personas = _read_json(PERSONAS_PATH)
    with open(MATRIX_PATH, "r", encoding="utf-8") as handle:
        matrix = yaml.safe_load(handle)
    dims = matrix.get("dimensions", {})
    allow_empty = bool(matrix.get("validation_rules", {}).get("allow_empty_segments", True))
    if allow_empty:
        return True
    keys = sorted(dims.keys())
    values = [dims[key]["values"] for key in keys]
    segments = set()
    for item in personas:
        segments.add(tuple(item[key] for key in keys))
    all_segments = set()
    def _recurse(idx: int, current: list) -> None:
        if idx == len(keys):
            all_segments.add(tuple(current))
            return
        for val in values[idx]:
            _recurse(idx + 1, current + [val])
    _recurse(0, [])
    return all_segments.issubset(segments)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    constraints = []

    matrix_ok = MATRIX_PATH.exists()
    constraints.append(_constraint("persona_matrix_exists", matrix_ok))
    constraints.append(_constraint("persona_matrix_versioned_v0.1", _check_matrix_version()))

    output_paths = [PERSONAS_PATH, DISTRIBUTION_PATH, RUN_METADATA_PATH]
    for path in output_paths:
        constraints.append(_constraint(f"output_exists:{path.name}", path.exists()))

    personas_sorted = False
    if PERSONAS_PATH.exists():
        personas = _read_json(PERSONAS_PATH)
        if isinstance(personas, list):
            sorted_copy = sorted(personas, key=lambda item: item.get("id", ""))
            personas_sorted = personas == sorted_copy
    constraints.append(_constraint("personas_deterministic_order", personas_sorted))
    constraints.append(_constraint("personas_include_all_dimensions", _check_persona_dimensions()))
    constraints.append(_constraint("no_empty_segments_when_disallowed", _check_empty_segments()))

    matrix_version = None
    factory_hash = None
    try:
        matrix_version = _load_matrix_version()
        factory_hash = compute_factory_hash()
        constraints.append(_constraint("factory_hash_computed", True))
    except Exception as exc:
        constraints.append(_constraint("factory_hash_computed", False, str(exc)))

    output_hashes = {}
    all_outputs = output_paths + [VALIDATION_PATH]
    for path in all_outputs:
        if path.exists():
            output_hashes[path.name] = _hash_file(path)

    run_metadata_ok = False
    if RUN_METADATA_PATH.exists():
        run_metadata = _read_json(RUN_METADATA_PATH)
        expected_hashes = run_metadata.get("output_hashes", {})
        expected = {
            PERSONAS_PATH.name: output_hashes.get(PERSONAS_PATH.name),
            DISTRIBUTION_PATH.name: output_hashes.get(DISTRIBUTION_PATH.name),
        }
        run_metadata_ok = expected_hashes == expected
    constraints.append(_constraint("output_hashes_match_run_metadata", run_metadata_ok))

    validation_report = {
        "matrix_version": matrix_version,
        "factory_hash": factory_hash,
        "script_versions": {
            "validate_personas.py": __version__,
            "factory_hash.py": factory_hash_version,
        },
        "constraints": constraints,
        "output_hashes": output_hashes,
    }

    _write_json(VALIDATION_PATH, validation_report)

    validation_hash = _hash_file(VALIDATION_PATH)
    validation_report["validation_report_hash"] = validation_hash
    _write_json(VALIDATION_PATH, validation_report)

    failures = [c for c in constraints if c["status"] == "fail"]
    validation_report["failed_constraints"] = failures
    _write_json(VALIDATION_PATH, validation_report)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
