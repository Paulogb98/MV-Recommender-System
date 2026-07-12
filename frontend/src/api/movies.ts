import { apiGet } from "./client";
import type { Movie, MovieFilters } from "../types";

export function searchMovies(query: string, filters: MovieFilters = {}, limit = 8): Promise<Movie[]> {
  return apiGet<Movie[]>("/api/movies/search", {
    q: query,
    genre: filters.genre,
    year_min: filters.yearMin,
    year_max: filters.yearMax,
    min_rating: filters.minRating,
    limit,
  });
}
