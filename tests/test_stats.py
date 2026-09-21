import pytest

from app.services.stats import accuracy, compute, consistency, raw, wpm

TARGET = "the quick brown fox jumps"  # 21 letters; 4 spaces credited (after all but last word)


def test_perfect_run():
    # 21 letters + 4 credited spaces = 25 chars in correct words -> 25/5 = 5.0 wpm over 60s
    assert wpm(TARGET, TARGET, 60) == pytest.approx(25 / 5)
    assert accuracy(TARGET, TARGET) == 100.0
    assert raw(TARGET, 60) == pytest.approx(21 / 5)
    r = compute(TARGET, TARGET, duration=60, per_second=[25] * 4)
    assert r["errors"] == 0
    assert r["correct"] == 25
    assert r["chars"] == 21


def test_all_wrong():
    typed = "zzz zzzzz zzzzz zzz zzzzz"  # same lengths, zero correct chars
    r = compute(TARGET, typed, duration=60)
    assert r["wpm"] == 0.0
    assert r["accuracy"] == 0.0
    assert r["errors"] == r["chars"] == 21


def test_empty_input():
    r = compute(TARGET, "", duration=60)
    assert r == {
        "wpm": 0.0,
        "raw": 0.0,
        "accuracy": 0.0,
        "consistency": 0.0,
        "chars": 0,
        "correct": 0,
        "errors": 0,
        "duration": 60,
    }


def test_extra_chars():
    # "thee" for "the": 3 correct keypresses, 1 wrong -> 75%; raw counts all 4 chars;
    # word isn't fully correct -> earns 0 wpm chars
    r = compute("the", "thee", duration=60)
    assert r["accuracy"] == 75.0
    assert r["chars"] == 4
    assert r["errors"] == 1
    assert r["wpm"] == 0.0


def test_skipped_word_does_not_crash():
    r = compute("the quick brown", "the brown", duration=60)
    assert r["errors"] >= 1


def test_single_second_run():
    # 25 correct chars in 1s: minutes = 1/60 -> 25/5*60 = 300 wpm
    assert wpm(TARGET, TARGET, 1) == pytest.approx(300.0)


def test_duration_guard():
    with pytest.raises(ValueError):
        wpm(TARGET, TARGET, 0)


def test_consistency_flat():
    assert consistency([40, 40, 40, 40]) == 100.0


def test_consistency_wild():
    # [10, 90]: mean 50, pstdev 40 -> cv 0.8 -> tanh(1.0362) = 0.7764 -> 22.36
    assert consistency([10, 90]) == pytest.approx(22.36, abs=0.05)
    assert consistency([10, 90]) < 60


def test_consistency_zero_mean():
    assert consistency([0, 0, 0]) == 0.0


def test_consistency_one_sample():
    assert consistency([50]) == 100.0  # stdev of a single value is 0 -> cv 0


def test_compute_returns_exact_keys():
    r = compute(TARGET, TARGET, duration=60, per_second=[20, 30, 40, 50, 60])
    assert set(r) == {
        "wpm",
        "raw",
        "accuracy",
        "consistency",
        "chars",
        "correct",
        "errors",
        "duration",
    }
