def test_search_by_title(client):
    response = client.get("/api/movies/search", params={"q": "toy"})
    assert response.status_code == 200
    titles = [m["title"] for m in response.json()]
    assert titles == ["Toy Story"]


def test_search_with_genre_filter(client):
    response = client.get("/api/movies/search", params={"genre": "Crime"})
    assert response.status_code == 200
    titles = [m["title"] for m in response.json()]
    assert titles == ["Heat"]


def test_search_null_tmdb_id_serializes_as_none(client):
    response = client.get("/api/movies/search", params={"q": "no poster"})
    assert response.status_code == 200
    [movie] = response.json()
    assert movie["tmdb_id"] is None


def test_recommendations_endpoint(client):
    response = client.post("/api/recommendations", json={"movie_ids": [1, 2], "n": 5})
    assert response.status_code == 200
    result_ids = [m["movie_id"] for m in response.json()]
    assert result_ids == [3]


def test_recommendations_rejects_more_than_three_movies(client):
    response = client.post("/api/recommendations", json={"movie_ids": [1, 2, 3, 4], "n": 5})
    assert response.status_code == 422
