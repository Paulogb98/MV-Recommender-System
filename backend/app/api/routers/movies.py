from fastapi import APIRouter, Depends, Query

from app.api.deps import get_catalog_service
from app.schemas.movie import MovieOut
from app.services.catalog_service import CatalogService

router = APIRouter(prefix="/api/movies", tags=["movies"])


@router.get("/search", response_model=list[MovieOut])
def search_movies(
    q: str = Query("", max_length=200),
    genre: str | None = None,
    year_min: int | None = None,
    year_max: int | None = None,
    min_rating: float | None = Query(None, ge=0, le=5),
    limit: int = Query(8, ge=1, le=50),
    catalog: CatalogService = Depends(get_catalog_service),
):
    return catalog.search(
        q=q, genre=genre, year_min=year_min, year_max=year_max, min_rating=min_rating, limit=limit
    )
