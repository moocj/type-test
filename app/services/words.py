"""
Loads the word list and generates words for testing.
"""

import json
import random
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Only fetch plain files
SAFE_NAME = re.compile(r"[a-z0-9_]+")

_lists: dict[str, list[str]] = {}


class UnknownListError(ValueError):
    """Error if the list doesn't exist (for testing purposes)."""


def load_list(name: str) -> list[str]:
    if not SAFE_NAME.fullmatch(name):
        raise UnknownListError(name)

    # If the list is new, add it, otherwise return an error.
    if name not in _lists:
        path = DATA_DIR / f"{name}.json"
        if not path.is_file():
            raise UnknownListError
        _lists[name] = json.loads(path.read_text(encoding="utf-8"))
    return _lists[name]


def generate(
    count: int, list_name: str = "english_1k", seed: int | None = None
) -> list[str]:
    words = load_list(list_name)
    # Generate a random seed for each request to keep it unique on the request itself
    rng = random.Random(seed) if seed is not None else random
    out: list[str] = []
    for _ in range(count):
        word = rng.choice(words)
        # No repeats within 10 words
        for _retry in range(10):
            if not out or word != out[-1]:
                break
            word = rng.choice(words)
        else:
            i = words.index(word)
            word = words[(i + 1) % len(words)]
        out.append(word)

    return out
