# ML Pipeline

Generates the compact serving artifacts used by the backend (`ml/artifacts/*.parquet`)
from the raw MovieLens dataset.

## Generated artifacts

| File | Content |
|---|---|
| `movie_neighbors.parquet` | Top-K neighbors per movie (item-item, cosine similarity) |
| `movie_metadata.parquet` | Title, year, genres, tmdb_id, average rating, number of ratings |
| `trending.parquet` | Movies ranked by popularity (Bayesian weighted rating) |

These 3 files are versioned in git (a few MB total) — the app works right after
cloning, with no need to download `ratings.csv` or retrain anything.

## Retraining with a new/updated dataset

1. Download a MovieLens dataset from https://grouplens.org/datasets/movielens/ and
   extract `ratings.csv`, `movies.csv`, and `links.csv` into `data/` (see
   [`data/README.md`](../data/README.md)).
2. Run the pipeline from the repo root:

```bash
uv sync --extra ml
uv run python -m ml.train
```

3. The 3 files in `ml/artifacts/` are regenerated. Restart the backend to reload
   them (artifacts are read once at startup).

## Hyperparameters (`ml/config.py`)

- `K_NEIGHBORS = 25` — neighbors pre-computed per movie.
- `MIN_RATINGS_FOR_NEIGHBORS = 5` — movies with fewer ratings than this are excluded
  from the neighbors artifact (similarity isn't reliable with too little data), but
  remain searchable in autocomplete via `movie_metadata.parquet`.
- `KNN_BATCH_SIZE = 5000` — batch size when running `kneighbors`, avoids RAM spikes.
