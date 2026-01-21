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


def _load_matrix() -> dict:
    if not MATRIX_PATH.exists():
        raise FileNotFoundError(f"matrix not found: {MATRIX_PATH}")
    with open(MATRIX_PATH, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("matrix must be a YAML mapping")
    if "version" not in data:
        raise ValueError("matrix missing version")
    if "global_constraints" not in data:
        raise ValueError("matrix missing global_constraints")
    if "total_personas" not in data["global_constraints"]:
        raise ValueError("matrix missing total_personas")
    if "dimensions" not in data:
        raise ValueError("matrix missing dimensions")
    if "archetypes" not in data:
        raise ValueError("matrix missing archetypes")
    if "validation_rules" not in data:
        raise ValueError("matrix missing validation_rules")
    return data


def _stable_persona_key(item: dict) -> str:
    return str(item["id"])


def _normalize_personas(personas: list[dict]) -> list[dict]:
    normalized = []
    for item in personas:
        if not isinstance(item, dict):
            raise ValueError("persona entry must be a mapping")
        normalized.append(item)
    return sorted(normalized, key=_stable_persona_key)


def _write_json(path: Path, payload: object) -> None:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    path.write_text(text, encoding="utf-8")


def _hash_file(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def _distribution_report(personas: list[dict]) -> dict:
    by_archetype = {}
    by_domain = {}
    for item in personas:
        archetype = str(item["archetype"])
        domain = str(item["domain"])
        by_archetype[archetype] = by_archetype.get(archetype, 0) + 1
        by_domain[domain] = by_domain.get(domain, 0) + 1
    return {
        "total_count": len(personas),
        "by_archetype": by_archetype,
        "by_domain": by_domain,
    }


def _dimension_combinations(dimensions: dict) -> list[dict]:
    keys = sorted(dimensions.keys())
    values = [list(dimensions[key]["values"]) for key in keys]
    combos = []

    def _recurse(idx: int, current: dict) -> None:
        if idx == len(keys):
            combos.append(current.copy())
            return
        key = keys[idx]
        for value in values[idx]:
            current[key] = value
            _recurse(idx + 1, current)

    _recurse(0, {})
    return combos


def _combo_key(combo: dict) -> tuple:
    return tuple(combo[key] for key in sorted(combo.keys()))


def _allocate_counts(total: int, weights: list[float]) -> list[int]:
    if total < 0:
        raise ValueError("total must be non-negative")
    weight_sum = sum(weights)
    if weight_sum <= 0:
        raise ValueError("weights must sum to > 0")
    raw = [total * w / weight_sum for w in weights]
    counts = [int(val) for val in raw]
    remainder = total - sum(counts)
    fractional = [val - int(val) for val in raw]
    order = sorted(
        range(len(weights)),
        key=lambda idx: (fractional[idx], -weights[idx], idx),
        reverse=True,
    )
    for idx in order[:remainder]:
        counts[idx] += 1
    return counts


def _generate_personas(matrix: dict) -> list[dict]:
    total_personas = int(matrix["global_constraints"]["total_personas"])
    dimensions = matrix["dimensions"]
    archetypes = list(matrix["archetypes"])
    rules = matrix["validation_rules"]
    allow_empty = bool(rules["allow_empty_segments"])

    combos = _dimension_combinations(dimensions)
    combos = sorted(combos, key=_combo_key)
    if not combos:
        raise ValueError("no dimension combinations found")

    if total_personas < len(combos) * len(archetypes) and not allow_empty:
        raise ValueError("total_personas too small to fill all segments")

    archetypes_sorted = sorted(archetypes, key=lambda item: str(item["id"]))
    archetype_count = len(archetypes_sorted)
    per_arch = total_personas // archetype_count
    remainder = total_personas % archetype_count

    personas = []
    for index, archetype in enumerate(archetypes_sorted):
        name = str(archetype["id"])
        assigned_total = per_arch + (1 if index < remainder else 0)
        weights = []
        for combo in combos:
            weight = 1.0
            for dim_name, dim_value in combo.items():
                weight *= float(archetype["weights"][dim_name][dim_value])
            weights.append(weight)

        counts = _allocate_counts(assigned_total, weights)
        if not allow_empty:
            counts = [max(1, count) for count in counts]
            if sum(counts) != assigned_total:
                diff = sum(counts) - assigned_total
                for idx in range(len(counts)):
                    if diff == 0:
                        break
                    if counts[idx] > 1:
                        counts[idx] -= 1
                        diff -= 1
                if diff != 0:
                    raise ValueError("unable to satisfy non-empty segments")

        for combo, count in zip(combos, counts):
            for offset in range(count):
                persona_id = f"{name}-{combo['seniority']}-{combo['domain']}-{combo['company_size']}-{offset}"
                persona = {
                    "id": persona_id,
                    "archetype": name,
                    "seniority": combo["seniority"],
                    "domain": combo["domain"],
                    "company_size": combo["company_size"],
                }
                personas.append(persona)

    return _normalize_personas(personas)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    matrix = _load_matrix()
    personas = _generate_personas(matrix)

    _write_json(PERSONAS_PATH, personas)
    _write_json(DISTRIBUTION_PATH, _distribution_report(personas))

    output_hashes = {
        PERSONAS_PATH.name: _hash_file(PERSONAS_PATH),
        DISTRIBUTION_PATH.name: _hash_file(DISTRIBUTION_PATH),
    }

    run_metadata = {
        "matrix_version": matrix["version"],
        "factory_hash": compute_factory_hash(),
        "output_hashes": output_hashes,
        "script_versions": {
            "generate_personas.py": __version__,
            "factory_hash.py": factory_hash_version,
        },
        "run_timestamp_utc": "1970-01-01T00:00:00Z",
    }
    _write_json(RUN_METADATA_PATH, run_metadata)


if __name__ == "__main__":
    main()
