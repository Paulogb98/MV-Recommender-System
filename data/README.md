# Dataset

This folder holds the raw [MovieLens](https://grouplens.org/datasets/movielens/) CSVs
used only for retraining the model (see [`ml/README.md`](../ml/README.md)). The app
itself doesn't need any of this to run — it ships with the pre-computed artifacts in
[`ml/artifacts/`](../ml/artifacts).

Download a MovieLens dataset and extract these 3 files here:

| File | Content |
|---|---|
| `ratings.csv` | `userId, movieId, rating, timestamp` |
| `movies.csv` | `movieId, title, genres` |
| `links.csv` | `movieId, imdbId, tmdbId` |

All three are gitignored (`data/*.csv`) — they're never committed to the repo.
