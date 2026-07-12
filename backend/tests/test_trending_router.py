def test_trending_returns_sorted_with_metadata(client):
    response = client.get("/api/trending", params={"limit": 2})
    assert response.status_code == 200
    body = response.json()
    assert [m["movie_id"] for m in body] == [3, 1]
    assert body[0]["title"] == "Heat"


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
