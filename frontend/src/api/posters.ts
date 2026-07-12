import { apiGet } from "./client";
import type { Poster } from "../types";

const cache = new Map<number, Promise<Poster | null>>();

export function fetchPoster(movieId: number): Promise<Poster | null> {
  if (!cache.has(movieId)) {
    cache.set(
      movieId,
      apiGet<Poster>(`/api/posters/${movieId}`).catch(() => null),
    );
  }
  return cache.get(movieId)!;
}
