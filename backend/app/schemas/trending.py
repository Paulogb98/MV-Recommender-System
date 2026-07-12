from app.schemas.movie import MovieOut


class TrendingItem(MovieOut):
    trending_score: float
