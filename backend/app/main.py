from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import movies, posters, recommendations, trending
from app.core.config import get_settings
from app.services.catalog_service import CatalogService
from app.services.poster_service import PosterService
from app.services.recommender_service import RecommenderService
from app.services.trending_service import TrendingService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Artifacts loaded once at startup (not on every request).
    settings = get_settings()
    app.state.catalog = CatalogService(settings.artifacts_dir / settings.metadata_file)
    app.state.recommender = RecommenderService(
        settings.artifacts_dir / settings.neighbors_file, app.state.catalog
    )
    app.state.trending = TrendingService(settings.artifacts_dir / settings.trending_file, app.state.catalog)
    app.state.poster = PosterService(settings)
    yield
    await app.state.poster.aclose()


app = FastAPI(title="MV Recommender API", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies.router)
app.include_router(recommendations.router)
app.include_router(trending.router)
app.include_router(posters.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
