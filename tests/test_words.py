import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.words import UnknownListError, generate, load_list

client = TestClient(app)


# --- service ---------------------------------------------------------------


def test_load_list_shape():
    words = load_list("english_1k")
    assert len(words) == 1000
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words)


def test_generate_respects_count():
    assert len(generate(37, seed=1)) == 37


def test_seed_is_stable():
    assert generate(50, list_name="english_1k", seed=42) == generate(
        50, list_name="english_1k", seed=42
    )


def test_unseeded_runs_differ():
    # 500 draws from 1000 words: identical twice is (1/1000)**499 - effectively impossible
    assert generate(500) != generate(500)


def test_no_immediate_repeats():
    words = generate(500, seed=7)
    assert all(a != b for a, b in zip(words, words[1:]))


def test_unknown_list_raises():
    with pytest.raises(UnknownListError):
        load_list("nope")


def test_path_traversal_rejected():
    with pytest.raises(UnknownListError):
        load_list("../main")


# --- http ------------------------------------------------------------------


def test_endpoint_defaults():
    r = client.get("/api/words")
    assert r.status_code == 200
    assert len(r.json()) == 50


def test_count_out_of_range_is_422():
    assert client.get("/api/words?count=0").status_code == 422
    assert client.get("/api/words?count=501").status_code == 422


def test_unknown_list_is_404():
    r = client.get("/api/words?list=nope")
    assert r.status_code == 404
    assert "nope" in r.json()["detail"]


def test_seed_is_stable_over_http():
    url = "/api/words?count=5&list=english_1k&seed=1"
    assert client.get(url).json() == client.get(url).json()


def test_static_still_mounted():
    # guards the route-order trap: routers must stay above mount("/")
    assert client.get("/index.html").status_code == 200
