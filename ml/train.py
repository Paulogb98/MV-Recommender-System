"""Trains the item-item KNN model and generates the compact serving artifacts.

Usage: python -m ml.train
"""
import time

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

from ml.config import ARTIFACTS_DIR, K_NEIGHBORS, KNN_BATCH_SIZE, MIN_RATINGS_FOR_NEIGHBORS
from ml.data import create_item_user_matrix, load_links, load_movies, load_ratings
from ml.export import build_movie_metadata, export_artifacts
from ml.trending import compute_rating_stats, compute_trending


def build_knn_neighbors(
    X,
    movie_inv_mapper: dict,
    eligible_indices: np.ndarray,
    k: int = K_NEIGHBORS,
    batch_size: int = KNN_BATCH_SIZE,
) -> pd.DataFrame:
    """Generates the top-k neighbors (cosine similarity) for each eligible movie.

    Runs `kneighbors` in batches over the X matrix itself, using sklearn's public
    API rather than accessing the private `_fit_X` attribute.
    """
    knn = NearestNeighbors(algorithm="brute", metric="cosine", n_jobs=-1)
    knn.fit(X)

    rows: list[tuple[int, int, int, float]] = []
    for start in range(0, len(eligible_indices), batch_size):
        batch_idx = eligible_indices[start : start + batch_size]
        distances, indices = knn.kneighbors(X[batch_idx], n_neighbors=k + 1)

        for row_pos, movie_idx in enumerate(batch_idx):
            rank = 0
            for dist, neighbor_idx in zip(distances[row_pos], indices[row_pos]):
                if neighbor_idx == movie_idx:
                    continue
                rank += 1
                if rank > k:
                    break
                score = 1.0 - float(dist)
                rows.append((movie_inv_mapper[movie_idx], movie_inv_mapper[neighbor_idx], rank, score))

    return pd.DataFrame(rows, columns=["movie_id", "neighbor_id", "rank", "score"])


def main() -> None:
    t0 = time.time()
    print("Loading ratings.csv...")
    ratings = load_ratings()
    print(f"  {len(ratings):,} ratings loaded in {time.time() - t0:.1f}s")

    print("Building sparse item-user matrix...")
    X, movie_mapper, _, movie_inv_mapper, _ = create_item_user_matrix(ratings)
    print(f"  {X.shape[0]:,} movies x {X.shape[1]:,} users matrix")

    print("Computing rating stats per movie...")
    rating_stats = compute_rating_stats(ratings)

    eligible_movie_ids = rating_stats.loc[rating_stats["n_ratings"] >= MIN_RATINGS_FOR_NEIGHBORS, "movieId"]
    eligible_indices = np.array([movie_mapper[mid] for mid in eligible_movie_ids if mid in movie_mapper])
    print(f"  {len(eligible_indices):,} movies eligible for neighbors (>= {MIN_RATINGS_FOR_NEIGHBORS} ratings)")

    print(f"Computing top-{K_NEIGHBORS} neighbors (KNN cosine, in batches of {KNN_BATCH_SIZE})...")
    t1 = time.time()
    neighbors_df = build_knn_neighbors(X, movie_inv_mapper, eligible_indices)
    print(f"  {len(neighbors_df):,} movie-neighbor pairs generated in {time.time() - t1:.1f}s")

    print("Computing trending (Bayesian weighted rating)...")
    trending_df = compute_trending(rating_stats)

    print("Building metadata (movies.csv + links.csv + stats)...")
    movies = load_movies()
    links = load_links()
    metadata_df = build_movie_metadata(movies, links, rating_stats)

    print("Exporting artifacts to ml/artifacts/...")
    export_artifacts(neighbors_df, metadata_df, trending_df)

    for f in sorted(ARTIFACTS_DIR.glob("*.parquet")):
        print(f"  {f.name}: {f.stat().st_size / 1024 / 1024:.2f} MB")

    print(f"Done in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
