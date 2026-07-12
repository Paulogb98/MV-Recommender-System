from fastapi import APIRouter, Depends

from app.api.deps import get_recommender_service
from app.schemas.recommendation import RecommendationOut, RecommendationRequest
from app.services.recommender_service import RecommenderService

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.post("", response_model=list[RecommendationOut])
def get_recommendations(
    payload: RecommendationRequest,
    recommender: RecommenderService = Depends(get_recommender_service),
):
    return recommender.recommend(payload.movie_ids, payload.n)
