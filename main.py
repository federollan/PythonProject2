from __future__ import annotations

import os
import sys


def load_environment_variables() -> None:
    """Load environment variables from a local .env file.

    Tries python-dotenv if available; otherwise, performs a minimal manual parse
    of a .env file in the current working directory.
    """
    loaded_with_dotenv = False
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
        loaded_with_dotenv = True
    except Exception:
        # If python-dotenv is not installed or fails, skip to manual load.
        pass

    if loaded_with_dotenv:
        return

    dotenv_path = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(dotenv_path):
        return

    try:
        with open(dotenv_path, "r", encoding="utf-8") as env_file:
            for raw_line in env_file:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except Exception:
        # Silently ignore manual .env loading errors.
        pass


def get_required_env_var(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Required environment variable '{name}' is not set. "
            f"Create a .env file with {name}=... or export it in your shell."
        )
    return value


def main() -> None:
    load_environment_variables()

    api_key = get_required_env_var("API_KEY")

    # Avoid printing secrets. Show only metadata.
    print(f"API key loaded. Length: {len(api_key)} characters.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)