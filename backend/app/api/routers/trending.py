from fastapi import APIRouter, Depends, Query

from app.api.deps import get_trending_service
from app.schemas.trending import TrendingItem
from app.services.trending_service import TrendingService

router = APIRouter(prefix="/api/trending", tags=["trending"])


@router.get("", response_model=list[TrendingItem])
def get_trending(
    limit: int = Query(10, ge=1, le=50),
    trending: TrendingService = Depends(get_trending_service),
):
    return trending.get_top(limit)
