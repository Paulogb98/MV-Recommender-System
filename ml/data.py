"""Loading of raw MovieLens data."""
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

from ml.config import LINKS_CSV, MOVIES_CSV, RATINGS_CHUNK_SIZE, RATINGS_CSV

RATINGS_DTYPES = {"userId": "int32", "movieId": "int32", "rating": "float32"}


def load_ratings() -> pd.DataFrame:
    """Reads ratings.csv in chunks with lean dtypes, reducing memory footprint."""
    chunks = pd.read_csv(
        RATINGS_CSV,
        usecols=["userId", "movieId", "rating"],
        dtype=RATINGS_DTYPES,
        chunksize=RATINGS_CHUNK_SIZE,
    )
    return pd.concat(chunks, ignore_index=True)


def load_movies() -> pd.DataFrame:
    return pd.read_csv(MOVIES_CSV, dtype={"movieId": "int32", "title": str, "genres": str})


def load_links() -> pd.DataFrame:
    links = pd.read_csv(LINKS_CSV, dtype={"movieId": "int32"})
    links["tmdbId"] = links["tmdbId"].astype("Int64")
    links["imdbId"] = links["imdbId"].astype("Int64")
    return links


def create_item_user_matrix(ratings: pd.DataFrame):
    """Builds the sparse movie x user matrix (CSR) for item-item recommendation.

    Same logic as recommender/model.ipynb, just ported into a reusable module.
    """
    unique_movies = np.unique(ratings["movieId"])
    unique_users = np.unique(ratings["userId"])
    m = len(unique_movies)
    n = len(unique_users)

    movie_mapper = dict(zip(unique_movies, range(m)))
    user_mapper = dict(zip(unique_users, range(n)))
    movie_inv_mapper = dict(zip(range(m), unique_movies))
    user_inv_mapper = dict(zip(range(n), unique_users))

    movie_index = ratings["movieId"].map(movie_mapper).to_numpy()
    user_index = ratings["userId"].map(user_mapper).to_numpy()

    X = csr_matrix((ratings["rating"], (movie_index, user_index)), shape=(m, n))
    return X, movie_mapper, user_mapper, movie_inv_mapper, user_inv_mapper
