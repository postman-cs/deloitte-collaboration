"""Generate a fresh OpenAPI spec and convert it to a Postman collection.

Usage:
    uv run python scripts/generate_openapi.py

Outputs:
    docs/api/openapi.json       — the raw OpenAPI 3.1 spec
"""

import json
from pathlib import Path

from src.app.main import app


def main() -> None:
    spec = app.openapi()

    # Write OpenAPI spec
    api_dir = Path("docs/api")
    api_dir.mkdir(parents=True, exist_ok=True)
    openapi_path = api_dir / "openapi.json"
    openapi_path.write_text(json.dumps(spec, indent=2))
    print(f"✅ OpenAPI spec written to {openapi_path}")  # noqa: T201

    print(  # noqa: T201
        "\n💡 To convert to a Postman collection, run:\n"
        "   npx openapi-to-postmanv2 -s docs/api/openapi.json -o docs/postman/collection.json -p"
    )


if __name__ == "__main__":
    main()
