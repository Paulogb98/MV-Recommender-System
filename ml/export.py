"""Builds the metadata table and writes the final artifacts to parquet."""
import re

import pandas as pd

from ml.config import ARTIFACTS_DIR, METADATA_PARQUET, NEIGHBORS_PARQUET, TRENDING_PARQUET

YEAR_RE = re.compile(r"\((\d{4})\)\s*$")


def parse_title_year(title: str) -> tuple[str, int | None]:
    match = YEAR_RE.search(title)
    if not match:
        return title, None
    year = int(match.group(1))
    clean_title = title[: match.start()].strip()
    return clean_title, year


def build_movie_metadata(movies: pd.DataFrame, links: pd.DataFrame, rating_stats: pd.DataFrame) -> pd.DataFrame:
    """Joins movies.csv + links.csv + rating stats into a single metadata artifact.

    Extracts the year from the title (format "Title (YYYY)") and turns genres into
    a list, since movies.csv doesn't have these as separate columns.
    """
    movies = movies.copy()
    parsed = movies["title"].apply(parse_title_year)
    movies["title"] = [p[0] for p in parsed]
    movies["year"] = pd.array([p[1] for p in parsed], dtype="Int64")
    movies["genres"] = movies["genres"].apply(lambda g: [] if g == "(no genres listed)" else g.split("|"))

    merged = movies.merge(links[["movieId", "tmdbId", "imdbId"]], on="movieId", how="left")
    merged = merged.merge(rating_stats, on="movieId", how="left")
    merged["n_ratings"] = merged["n_ratings"].fillna(0).astype("int32")
    merged["avg_rating"] = merged["avg_rating"].astype("float32")

    return merged.rename(columns={"movieId": "movie_id", "tmdbId": "tmdb_id", "imdbId": "imdb_id"})[
        ["movie_id", "title", "year", "genres", "tmdb_id", "imdb_id", "avg_rating", "n_ratings"]
    ]


def export_artifacts(neighbors_df: pd.DataFrame, metadata_df: pd.DataFrame, trending_df: pd.DataFrame) -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    neighbors_df.to_parquet(NEIGHBORS_PARQUET, index=False)
    metadata_df.to_parquet(METADATA_PARQUET, index=False)

    trending_out = trending_df.rename(columns={"movieId": "movie_id"})[["movie_id", "trending_score"]]
    trending_out.to_parquet(TRENDING_PARQUET, index=False)
