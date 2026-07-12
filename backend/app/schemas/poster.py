from pydantic import BaseModel


class PosterOut(BaseModel):
    tmdb_id: int
    title: str | None = None
    poster_url: str | None = None
