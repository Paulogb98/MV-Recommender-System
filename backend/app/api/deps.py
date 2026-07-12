from fastapi import Request

from app.services.catalog_service import CatalogService
from app.services.poster_service import PosterService
from app.services.recommender_service import RecommenderService
from app.services.trending_service import TrendingService


def get_catalog_service(request: Request) -> CatalogService:
    return request.app.state.catalog


def get_recommender_service(request: Request) -> RecommenderService:
    return request.app.state.recommender


def get_trending_service(request: Request) -> TrendingService:
    return request.app.state.trending


def get_poster_service(request: Request) -> PosterService:
    return request.app.state.poster
