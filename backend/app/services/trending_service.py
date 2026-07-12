from pathlib import Path

import pandas as pd

from app.services.catalog_service import CatalogService


class TrendingService:
    """Trending movies, computed offline (ml/trending.py) via Bayesian weighted rating."""

    def __init__(self, trending_path: Path, catalog_service: CatalogService):
        self._df = pd.read_parquet(trending_path)  # already sorted desc by trending_score
        self._catalog = catalog_service

    def get_top(self, limit: int = 10) -> list[dict]:
        top = self._df.head(limit)
        metadata = self._catalog.get_many(top["movie_id"].tolist())

        results = []
        for movie_id, score in zip(top["movie_id"], top["trending_score"]):
            meta = metadata.get(int(movie_id))
            if meta is None:
                continue
            results.append({**meta, "trending_score": round(float(score), 4)})
        return results
