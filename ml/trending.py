"""Popularity (trending) computation via IMDB-style weighted rating."""
import pandas as pd


def compute_rating_stats(ratings: pd.DataFrame) -> pd.DataFrame:
    """Aggregates rating count and average per movie."""
    stats = ratings.groupby("movieId")["rating"].agg(n_ratings="count", avg_rating="mean")
    return stats.reset_index()


def compute_trending(rating_stats: pd.DataFrame, percentile: float = 0.6) -> pd.DataFrame:
    """Computes the (Bayesian) weighted rating, same as the "IMDB Top 250":

    WR = (v / (v + m)) * R + (m / (v + m)) * C

    where v = the movie's n_ratings, R = the movie's avg_rating, m = minimum vote
    threshold (percentile of the n_ratings distribution), and C = global avg_rating
    mean. Prevents a movie with few 5.0 ratings from ranking above one with 50k
    ratings at 4.3.
    """
    v = rating_stats["n_ratings"]
    r = rating_stats["avg_rating"]
    m = v.quantile(percentile)
    c = r.mean()

    trending_score = (v / (v + m)) * r + (m / (v + m)) * c

    out = rating_stats.copy()
    out["trending_score"] = trending_score
    return out.sort_values("trending_score", ascending=False).reset_index(drop=True)
