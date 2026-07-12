from app.services.catalog_service import CatalogService
from app.services.recommender_service import RecommenderService


def test_recommend_excludes_selected_and_aggregates_scores(artifacts_dir):
    catalog = CatalogService(artifacts_dir / "movie_metadata.parquet")
    recommender = RecommenderService(artifacts_dir / "movie_neighbors.parquet", catalog)

    results = recommender.recommend([1, 2], n=5)
    result_ids = [r["movie_id"] for r in results]

    assert 1 not in result_ids
    assert 2 not in result_ids
    assert result_ids == [3]  # only common neighbor, score aggregated from both selections


def test_recommend_movie_without_neighbors_is_ignored(artifacts_dir):
    catalog = CatalogService(artifacts_dir / "movie_metadata.parquet")
    recommender = RecommenderService(artifacts_dir / "movie_neighbors.parquet", catalog)

    results = recommender.recommend([4], n=5)  # movie_id 4 has no neighbors in the artifact

    assert results == []
