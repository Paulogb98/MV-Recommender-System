import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import type { Movie } from "../types";

interface WatchlistContextValue {
  items: Movie[];
  isWatchlisted: (movieId: number) => boolean;
  add: (movie: Movie) => void;
  remove: (movieId: number) => void;
  toggle: (movie: Movie) => void;
}

const WatchlistContext = createContext<WatchlistContextValue | null>(null);
const STORAGE_KEY = "mv-watchlist";

function loadInitial(): Movie[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? (JSON.parse(raw) as Movie[]) : [];
  } catch {
    return [];
  }
}

export function WatchlistProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<Movie[]>(loadInitial);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  }, [items]);

  const value = useMemo<WatchlistContextValue>(() => {
    const isWatchlisted = (movieId: number) => items.some((m) => m.movie_id === movieId);
    const add = (movie: Movie) =>
      setItems((prev) => (prev.some((m) => m.movie_id === movie.movie_id) ? prev : [...prev, movie]));
    const remove = (movieId: number) => setItems((prev) => prev.filter((m) => m.movie_id !== movieId));
    const toggle = (movie: Movie) => (isWatchlisted(movie.movie_id) ? remove(movie.movie_id) : add(movie));
    return { items, isWatchlisted, add, remove, toggle };
  }, [items]);

  return <WatchlistContext.Provider value={value}>{children}</WatchlistContext.Provider>;
}

export function useWatchlist(): WatchlistContextValue {
  const ctx = useContext(WatchlistContext);
  if (!ctx) throw new Error("useWatchlist must be used within WatchlistProvider");
  return ctx;
}
