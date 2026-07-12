"""Configuration for the ML training and artifact export pipeline."""
from pathlib import Path

ML_DIR = Path(__file__).resolve().parent
ROOT_DIR = ML_DIR.parent

DATA_DIR = ROOT_DIR / "data"
RATINGS_CSV = DATA_DIR / "ratings.csv"
MOVIES_CSV = DATA_DIR / "movies.csv"
LINKS_CSV = DATA_DIR / "links.csv"

ARTIFACTS_DIR = ML_DIR / "artifacts"
NEIGHBORS_PARQUET = ARTIFACTS_DIR / "movie_neighbors.parquet"
METADATA_PARQUET = ARTIFACTS_DIR / "movie_metadata.parquet"
TRENDING_PARQUET = ARTIFACTS_DIR / "trending.parquet"

# Item-item model hyperparameters
K_NEIGHBORS = 25
MIN_RATINGS_FOR_NEIGHBORS = 5
KNN_BATCH_SIZE = 5000
RATINGS_CHUNK_SIZE = 1_000_000
