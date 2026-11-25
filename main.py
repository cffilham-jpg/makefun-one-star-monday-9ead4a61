"""Write the selected one-star review for Monday to the make.fun output file."""

import hashlib
import os
from pathlib import Path
import tempfile


# The waiter serving Monday as the dish gives the review one specific, diner-like twist.
# Validation keeps the emitted UTF-8 bytes on that exact one-line text.
LINE = "One star. The waiter sat me down and served me Monday."
CHAR_LIMIT = 180
WORD_LIMIT = 25


def _resolve_output_dir() -> Path:
    """Return a writable output directory, falling back to a temporary directory."""
    candidate = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    try:
        candidate.mkdir(parents=True, exist_ok=True)
        return candidate
    except OSError:
        return Path(tempfile.mkdtemp(prefix="makefun-output-"))


def validate(path: Path) -> None:
    """Assert that entry.txt contains exactly the permitted one-line review."""
    content = path.read_bytes()
    expected = LINE.encode("utf-8")
    assert content == expected
    text = content.decode("utf-8")
    assert 1 <= len(text) <= CHAR_LIMIT
    assert len(text.split()) <= WORD_LIMIT
    assert "\n" not in text and "\r" not in text
    assert not content.endswith((b"\n", b"\r"))
    assert text == text.strip()


def main() -> None:
    output_path = _resolve_output_dir() / "entry.txt"
    output_path.write_bytes(LINE.encode("utf-8"))
    validate(output_path)
    print(hashlib.sha256(LINE.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
