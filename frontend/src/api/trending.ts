import { apiGet } from "./client";
import type { TrendingItem } from "../types";

export function fetchTrending(limit = 10): Promise<TrendingItem[]> {
  return apiGet<TrendingItem[]>("/api/trending", { limit });
}
