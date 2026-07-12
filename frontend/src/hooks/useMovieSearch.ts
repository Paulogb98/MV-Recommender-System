import { useEffect, useState } from "react";
import { searchMovies } from "../api/movies";
import type { Movie, MovieFilters } from "../types";
import { useDebouncedValue } from "./useDebouncedValue";

export function useMovieSearch(query: string, filters: MovieFilters, excludeIds: number[]) {
  const debouncedQuery = useDebouncedValue(query, 250);
  const excludeKey = excludeIds.join(",");
  const [results, setResults] = useState<Movie[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    setIsLoading(true);

    searchMovies(debouncedQuery, filters, 8)
      .then((movies) => {
        if (cancelled) return;
        setResults(movies.filter((m) => !excludeIds.includes(m.movie_id)));
      })
      .catch(() => {
        if (!cancelled) setResults([]);
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [debouncedQuery, filters.genre, filters.yearMin, filters.yearMax, filters.minRating, excludeKey]);

  return { results, isLoading };
}
