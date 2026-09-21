"""
Converts typing data into statistics that can be tested and presented to the user.
Doesn't use clock instead just takes in whatever duration is being used to make it simpler.
"""

import math
import statistics

# Helper methods


def _minutes(duration: float) -> float:
    if duration <= 0:
        raise ValueError("duration must be positive")
    return duration / 60


def _rate(chars: int, duration: float) -> float:
    return chars / 5 / _minutes(duration)  # Take each word to be about 5 characters


def wpm(target: str, typed: str, duration: float) -> float:
    return _rate(_score(target, typed)[2], duration)


def raw(typed: str, duration: float) -> float:
    return _rate(sum(len(w) for w in typed.split()), duration)


def accuracy(target: str, typed: str) -> float:
    keypresses, ok, _, _ = _score(target, typed)
    return ok / keypresses * 100 if keypresses else 0.0


def consistency(per_second: list[float]) -> float:
    if not per_second:
        return 0.0
    mean = statistics.fmean(per_second)
    if mean <= 0:
        return 0.0
    cv = statistics.pstdev(per_second) / mean  # standard deviation / mean
    return 100.0 * (1 - math.tanh(cv + cv**3 / 3 + cv**5 / 5))


def _score(target: str, typed: str) -> tuple[int, int, int, int]:
    """
    Returns a tuple with keypresses, correct keypresses, correct characters and errors for calculation.
    """

    target_words = target.split()
    typed_words = typed.split()
    keypresses = correct_keypresses = correct_chars = errors = 0

    for i, t_word in enumerate(target_words):
        y_word = typed_words[i] if i < len(typed_words) else ""
        keypresses += len(y_word)
        for t_char, y_char in zip(t_word, y_word):
            if t_char == y_char:
                correct_keypresses += 1
            else:
                errors += 1
        extras = len(y_word) - len(t_word)
        if extras > 0:
            errors += extras  # words typed after a word is done
        if y_word and y_word == t_word:
            correct_chars += len(t_word)
            if i < len(target_words) - 1:
                correct_chars += 1

    for extra_word in typed_words[len(target_words) :]:
        keypresses += len(extra_word)
        errors += len(extra_word)

    return keypresses, correct_keypresses, correct_chars, errors


def compute(
    target: str, typed: str, duration: float = 60, per_second: list[float] | None = None
) -> dict:
    """
    Returns stats that the result screen can display.
    """
    keypresses, correct_keypresses, correct_chars, errors = _score(target, typed)
    return {
        "wpm": _rate(correct_chars, duration),
        "raw": _rate(keypresses, duration),
        "accuracy": correct_keypresses / keypresses * 100 if keypresses else 0.0,
        "consistency": consistency(per_second or []),
        "chars": keypresses,
        "correct": correct_chars,
        "errors": errors,
        "duration": duration,
    }
