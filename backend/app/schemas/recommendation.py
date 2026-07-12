from pydantic import BaseModel, Field

from app.schemas.movie import MovieOut


class RecommendationRequest(BaseModel):
    movie_ids: list[int] = Field(min_length=1, max_length=3)
    n: int = Field(default=5, ge=1, le=10)


class RecommendationOut(MovieOut):
    score: float
