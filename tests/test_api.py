import pytest

from app.services.stats import compute

PAYLOAD = {
    "target": "the quick brown fox",
    "typed": "the quick brown fox",
    "duration": 30,
    "per_second": [20, 30, 40],
    "mode": "time",
    "mode_value": 30,
    "list": "english_1k",
}


def test_post_stores_server_computed_stats(client):
    r = client.post("/api/results", json=PAYLOAD)
    assert r.status_code == 201
    row = r.json()
    expected = compute(
        PAYLOAD["target"], PAYLOAD["typed"], PAYLOAD["duration"], PAYLOAD["per_second"]
    )
    assert row["wpm"] == pytest.approx(expected["wpm"])
    assert row["raw"] == pytest.approx(expected["raw"])
    assert row["acc"] == pytest.approx(expected["accuracy"])
    assert row["consistency"] == pytest.approx(expected["consistency"])
    assert row["id"] is not None
    assert row["created_at"] is not None
    assert (row["target"], row["typed"], row["list"], row["mode"]) == (
        PAYLOAD["target"],
        PAYLOAD["typed"],
        PAYLOAD["list"],
        PAYLOAD["mode"],
    )


def test_post_rejects_client_supplied_wpm(client):
    assert client.post("/api/results", json={**PAYLOAD, "wpm": 999}).status_code == 422


def test_post_validates_input(client):
    for bad in ({"mode": "zen"}, {"duration": 0}, {"mode_value": 0}):
        assert client.post("/api/results", json={**PAYLOAD, **bad}).status_code == 422


def test_post_without_per_second_defaults_to_zero_consistency(client):
    payload = {k: v for k, v in PAYLOAD.items() if k != "per_second"}
    r = client.post("/api/results", json=payload)
    assert r.status_code == 201
    assert r.json()["consistency"] == 0.0


def test_get_is_newest_first(client):
    for value in (15, 30, 60):
        assert (
            client.post(
                "/api/results", json={**PAYLOAD, "mode_value": value}
            ).status_code
            == 201
        )
    rows = client.get("/api/results").json()
    assert [row["mode_value"] for row in rows] == [60, 30, 15]


def test_get_validates_limit(client):
    assert client.get("/api/results?limit=0").status_code == 422
    assert client.get("/api/results?limit=101").status_code == 422
    assert client.get("/api/results?limit=1").json() == []
