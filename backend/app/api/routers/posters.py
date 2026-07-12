from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_catalog_service, get_poster_service
from app.schemas.poster import PosterOut
from app.services.catalog_service import CatalogService
from app.services.poster_service import PosterService

router = APIRouter(prefix="/api/posters", tags=["posters"])


@router.get("/{movie_id}", response_model=PosterOut)
async def get_poster(
    movie_id: int,
    poster: PosterService = Depends(get_poster_service),
    catalog: CatalogService = Depends(get_catalog_service),
):
    identifiers = catalog.get_identifiers(movie_id)
    if identifiers is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    result = await poster.get_poster(movie_id, identifiers["tmdb_id"], identifiers["imdb_id"])
    if result is None:
        raise HTTPException(status_code=404, detail="Poster not found")
    return result
