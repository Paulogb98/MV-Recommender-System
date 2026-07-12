import asyncio
import time

import httpx

from app.core.config import Settings


class _NotFound(Exception):
    """Genuine 404: this tmdb_id isn't this media type, try the next fallback."""


class PosterService:
    """TMDB proxy: hides the API key from the client and returns only the public
    poster_url (TMDB CDN), without binary-proxying the image. In-memory cache with TTL.

    A fraction of MovieLens "movies" are actually TV series/documentaries
    (e.g. Planet Earth II, Band of Brothers) — the tmdbId from links.csv is
    sometimes invalid on both /movie and /tv (stale dataset). That's why the
    lookup cascades: /movie/{tmdb_id} -> /tv/{tmdb_id} -> /find/{imdb_id}.

    Only an explicit 404 advances to the next fallback. Any other error (429
    rate-limit, 5xx, timeout) aborts without caching — otherwise a burst of
    simultaneous poster requests (10 cards mounting at once) can get /movie
    rate-limited, fall through to /tv, and since TMDB's movie/TV id spaces are
    independent, hit a completely unrelated show by numeric coincidence and
    cache that wrong result for 24h.
    """

    def __init__(self, settings: Settings):
        self._settings = settings
        self._cache: dict[int, tuple[float, dict | None]] = {}
        self._client = httpx.AsyncClient(base_url=settings.tmdb_base_url, timeout=10.0)
        self._semaphore = asyncio.Semaphore(4)

    async def get_poster(self, movie_id: int, tmdb_id: int | None, imdb_id: int | None) -> dict | None:
        if not self._settings.tmdb_api_key:
            return None

        cached = self._cache.get(movie_id)
        now = time.monotonic()
        if cached is not None and now - cached[0] < self._settings.poster_cache_ttl_seconds:
            return cached[1]

        try:
            result = None
            if tmdb_id is not None:
                try:
                    result = await self._by_movie(tmdb_id)
                except _NotFound:
                    try:
                        result = await self._by_tv(tmdb_id)
                    except _NotFound:
                        result = None
            if result is None and imdb_id is not None:
                result = await self._by_imdb(imdb_id, fallback_id=tmdb_id)
        except httpx.HTTPError:
            return None

        self._cache[movie_id] = (now, result)
        return result

    async def _get(self, path: str, params: dict) -> dict:
        async with self._semaphore:
            response = await self._client.get(path, params={**params, "api_key": self._settings.tmdb_api_key})
        if response.status_code == 404:
            raise _NotFound
        response.raise_for_status()
        return response.json()

    async def _by_movie(self, tmdb_id: int) -> dict:
        data = await self._get(f"/movie/{tmdb_id}", {})
        return self._build_result(tmdb_id, data.get("title"), data.get("poster_path"))

    async def _by_tv(self, tmdb_id: int) -> dict:
        data = await self._get(f"/tv/{tmdb_id}", {})
        return self._build_result(tmdb_id, data.get("name"), data.get("poster_path"))

    async def _by_imdb(self, imdb_id: int, fallback_id: int | None) -> dict | None:
        try:
            data = await self._get(f"/find/tt{imdb_id:07d}", {"external_source": "imdb_id"})
        except _NotFound:
            return None
        hit = next(iter(data.get("movie_results") or []), None) or next(iter(data.get("tv_results") or []), None)
        if hit is None:
            return None
        return self._build_result(fallback_id or hit.get("id"), hit.get("title") or hit.get("name"), hit.get("poster_path"))

    def _build_result(self, tmdb_id: int | None, title: str | None, poster_path: str | None) -> dict:
        return {
            "tmdb_id": tmdb_id or 0,
            "title": title,
            "poster_url": f"{self._settings.tmdb_image_base_url}{poster_path}" if poster_path else None,
        }

    async def aclose(self) -> None:
        await self._client.aclose()
