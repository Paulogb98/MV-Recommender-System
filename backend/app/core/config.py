from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_DEFAULT_ARTIFACTS_DIR = Path(__file__).resolve().parents[3] / "ml" / "artifacts"


class Settings(BaseSettings):
    tmdb_api_key: str = ""
    tmdb_base_url: str = "https://api.themoviedb.org/3"
    tmdb_image_base_url: str = "https://image.tmdb.org/t/p/w500"
    cors_origins: list[str] = ["http://localhost:5173"]

    artifacts_dir: Path = _DEFAULT_ARTIFACTS_DIR
    neighbors_file: str = "movie_neighbors.parquet"
    metadata_file: str = "movie_metadata.parquet"
    trending_file: str = "trending.parquet"

    poster_cache_ttl_seconds: int = 60 * 60 * 24

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
