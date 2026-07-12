from pathlib import Path

import pandas as pd

from app.services.serialization import records_from_df


class CatalogService:
    """Movie metadata (title, year, genres, tmdb_id, rating stats).

    Loads the metadata parquet once into memory; serves search/autocomplete
    with genre/year/rating filters and batch lookup by movie_id.
    """

    def __init__(self, metadata_path: Path):
        df = pd.read_parquet(metadata_path)
        df["title_lower"] = df["title"].str.lower()
        self._df = df.set_index("movie_id", drop=False)

    def search(
        self,
        q: str = "",
        genre: str | None = None,
        year_min: int | None = None,
        year_max: int | None = None,
        min_rating: float | None = None,
        limit: int = 8,
    ) -> list[dict]:
        df = self._df
        if q:
            df = df[df["title_lower"].str.contains(q.lower(), regex=False, na=False)]
        if genre:
            df = df[df["genres"].apply(lambda genres: genre in genres)]
        if year_min is not None:
            df = df[df["year"] >= year_min]
        if year_max is not None:
            df = df[df["year"] <= year_max]
        if min_rating is not None:
            df = df[df["avg_rating"] >= min_rating]

        df = df.sort_values("n_ratings", ascending=False).head(limit)
        return records_from_df(df.drop(columns="title_lower"))

    def get_many(self, movie_ids: list[int]) -> dict[int, dict]:
        existing = [mid for mid in movie_ids if mid in self._df.index]
        if not existing:
            return {}
        subset = self._df.loc[existing].drop(columns="title_lower")
        records = records_from_df(subset)
        return {record["movie_id"]: record for record in records}

    def get_identifiers(self, movie_id: int) -> dict | None:
        """Raw tmdb_id/imdb_id (bypassing MovieOut) for the poster proxy."""
        if movie_id not in self._df.index:
            return None
        row = self._df.loc[movie_id]
        return {
            "tmdb_id": None if pd.isna(row["tmdb_id"]) else int(row["tmdb_id"]),
            "imdb_id": None if pd.isna(row["imdb_id"]) else int(row["imdb_id"]),
        }
