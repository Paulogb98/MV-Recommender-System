import { apiPost } from "./client";
import type { RecommendationResult } from "../types";

export function fetchRecommendations(movieIds: number[], n: number): Promise<RecommendationResult[]> {
  return apiPost<RecommendationResult[]>("/api/recommendations", { movie_ids: movieIds, n });
}
