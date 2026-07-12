import os

import pandas as pd
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def artifacts_dir(tmp_path_factory):
    """Small synthetic artifacts, without depending on the real 84k-movie dataset."""
    d = tmp_path_factory.mktemp("artifacts")

    metadata = pd.DataFrame(
        [
            {"movie_id": 1, "title": "Toy Story", "year": 1995, "genres": ["Animation", "Comedy"], "tmdb_id": 862, "avg_rating": 3.9, "n_ratings": 100},
            {"movie_id": 2, "title": "Jumanji", "year": 1995, "genres": ["Adventure", "Fantasy"], "tmdb_id": 8844, "avg_rating": 3.2, "n_ratings": 80},
            {"movie_id": 3, "title": "Heat", "year": 1995, "genres": ["Action", "Crime"], "tmdb_id": 949, "avg_rating": 4.0, "n_ratings": 60},
            {"movie_id": 4, "title": "No Poster Movie", "year": 2001, "genres": ["Drama"], "tmdb_id": None, "avg_rating": 2.5, "n_ratings": 6},
        ]
    )
    metadata.to_parquet(d / "movie_metadata.parquet", index=False)

    neighbors = pd.DataFrame(
        [
            {"movie_id": 1, "neighbor_id": 2, "rank": 1, "score": 0.8},
            {"movie_id": 1, "neighbor_id": 3, "rank": 2, "score": 0.5},
            {"movie_id": 2, "neighbor_id": 1, "rank": 1, "score": 0.8},
            {"movie_id": 2, "neighbor_id": 3, "rank": 2, "score": 0.3},
        ]
    )
    neighbors.to_parquet(d / "movie_neighbors.parquet", index=False)

    trending = pd.DataFrame(
        [
            {"movie_id": 3, "trending_score": 4.1},
            {"movie_id": 1, "trending_score": 3.9},
            {"movie_id": 2, "trending_score": 3.2},
        ]
    )
    trending.to_parquet(d / "trending.parquet", index=False)

    return d


@pytest.fixture(scope="session", autouse=True)
def _test_env(artifacts_dir):
    """Set env vars BEFORE any import of app.main (settings is read once, cached)."""
    os.environ["ARTIFACTS_DIR"] = str(artifacts_dir)
    os.environ["TMDB_API_KEY"] = "test-key"
    yield


@pytest.fixture()
def client(_test_env):
    from app.core.config import get_settings

    get_settings.cache_clear()
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
