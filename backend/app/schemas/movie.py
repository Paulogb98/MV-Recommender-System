from pydantic import BaseModel


class MovieOut(BaseModel):
    movie_id: int
    title: str
    year: int | None = None
    genres: list[str] = []
    tmdb_id: int | None = None
    avg_rating: float | None = None
    n_ratings: int = 0
