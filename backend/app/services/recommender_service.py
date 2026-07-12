from collections import defaultdict
from pathlib import Path

import pandas as pd

from app.services.catalog_service import CatalogService


class RecommenderService:
    """Item-item recommendation from pre-computed neighbors (offline, ml/train.py).

    Loads the neighbors parquet once at startup and keeps everything in memory,
    so no artifact is reloaded from disk on individual requests.
    """

    def __init__(self, neighbors_path: Path, catalog_service: CatalogService):
        df = pd.read_parquet(neighbors_path)
        self._neighbors: dict[int, list[tuple[int, float]]] = defaultdict(list)
        for movie_id, neighbor_id, score in zip(df["movie_id"], df["neighbor_id"], df["score"]):
            self._neighbors[int(movie_id)].append((int(neighbor_id), float(score)))
        self._catalog = catalog_service

    def recommend(self, movie_ids: list[int], n: int = 5) -> list[dict]:
        selected = set(movie_ids)
        scores: dict[int, float] = defaultdict(float)

        for movie_id in movie_ids:
            for neighbor_id, score in self._neighbors.get(movie_id, []):
                if neighbor_id in selected:
                    continue
                scores[neighbor_id] += score

        ranked_ids = sorted(scores, key=scores.get, reverse=True)[:n]
        metadata = self._catalog.get_many(ranked_ids)

        results = []
        for movie_id in ranked_ids:
            meta = metadata.get(movie_id)
            if meta is None:
                continue
            results.append({**meta, "score": round(scores[movie_id], 4)})
        return results
