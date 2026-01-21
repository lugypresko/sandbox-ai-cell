#!/usr/bin/env python3
from pathlib import Path


def check_file(path: Path) -> bool:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        print(f"{path}: invalid UTF-8")
        return False

    bad_count = 0
    non_ascii_count = 0
    for ch in text:
        code = ord(ch)
        if code < 32 and ch not in "\n\r\t":
            bad_count += 1
        elif code > 127:
            non_ascii_count += 1

    ok = True
    if bad_count:
        print(f"{path}: control characters found (count={bad_count})")
        ok = False
    if non_ascii_count:
        print(f"{path}: non-ASCII characters found (count={non_ascii_count})")
        ok = False
    return ok


def main() -> int:
    root = Path(".")
    ok = True
    for path in root.rglob("*.md"):
        if not check_file(path):
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
