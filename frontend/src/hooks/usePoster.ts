import { useEffect, useState } from "react";
import { fetchPoster } from "../api/posters";
import type { Poster } from "../types";

export function usePoster(movieId: number | null): Poster | null {
  const [poster, setPoster] = useState<Poster | null>(null);

  useEffect(() => {
    if (movieId == null) {
      setPoster(null);
      return;
    }
    let cancelled = false;
    fetchPoster(movieId).then((data) => {
      if (!cancelled) setPoster(data);
    });
    return () => {
      cancelled = true;
    };
  }, [movieId]);

  return poster;
}
