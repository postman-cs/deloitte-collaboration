"""Pre-commit hook: ensure Postman environment files don't contain real secrets.

Scans for environment files that have actual values in sensitive keys
(API keys, tokens, passwords, secrets). Only variable *placeholders*
({{VAR}} or empty strings) are allowed for these keys.
"""

import json
import re
import sys
from pathlib import Path

# Keys whose values must NOT contain real credentials
SENSITIVE_PATTERNS = re.compile(
    r"(api[_-]?key|token|secret|password|auth|credential|bearer)",
    re.IGNORECASE,
)

# Values considered "safe" (placeholders, empty, template vars)
SAFE_VALUE = re.compile(r"^(\{\{.*\}\}|<.*>|)$")


def check_file(path: Path) -> list[str]:
    violations: list[str] = []
    try:
        data = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        return [f"{path}: Could not parse — {e}"]

    values = data.get("values", [])
    for entry in values:
        key = entry.get("key", "")
        value = str(entry.get("value", ""))
        if SENSITIVE_PATTERNS.search(key) and not SAFE_VALUE.match(value):
            violations.append(
                f"{path}: Key '{key}' appears to contain a real secret. "
                f"Use a placeholder like '{{{{MY_VAR}}}}' instead."
            )
    return violations


def main() -> int:
    files = [Path(f) for f in sys.argv[1:]]
    all_violations: list[str] = []
    for f in files:
        all_violations.extend(check_file(f))

    if all_violations:
        print("❌ Postman environment secret check FAILED:")  # noqa: T201
        for v in all_violations:
            print(f"  • {v}")  # noqa: T201
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
