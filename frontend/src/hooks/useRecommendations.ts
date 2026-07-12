import { useCallback, useState } from "react";
import { fetchRecommendations } from "../api/recommendations";
import type { RecommendationResult } from "../types";

export type RecommendationStatus = "idle" | "loading" | "results" | "error";

export function useRecommendations() {
  const [status, setStatus] = useState<RecommendationStatus>("idle");
  const [results, setResults] = useState<RecommendationResult[]>([]);

  const submit = useCallback(async (movieIds: number[], n: number) => {
    setStatus("loading");
    try {
      const data = await fetchRecommendations(movieIds, n);
      setResults(data);
      setStatus("results");
    } catch {
      setResults([]);
      setStatus("error");
    }
  }, []);

  const reset = useCallback(() => {
    setStatus("idle");
    setResults([]);
  }, []);

  return { status, results, submit, reset };
}
