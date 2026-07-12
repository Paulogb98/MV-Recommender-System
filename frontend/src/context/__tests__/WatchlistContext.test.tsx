import { renderHook, act } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";
import { WatchlistProvider, useWatchlist } from "../WatchlistContext";
import type { Movie } from "../../types";

const MOVIE: Movie = {
  movie_id: 1,
  title: "Toy Story",
  year: 1995,
  genres: ["Animation"],
  tmdb_id: 862,
  avg_rating: 3.9,
  n_ratings: 100,
};

beforeEach(() => {
  localStorage.clear();
});

describe("WatchlistContext", () => {
  it("adds and persists a movie to localStorage", () => {
    const { result } = renderHook(() => useWatchlist(), { wrapper: WatchlistProvider });

    act(() => result.current.add(MOVIE));

    expect(result.current.isWatchlisted(1)).toBe(true);
    expect(JSON.parse(localStorage.getItem("mv-watchlist") ?? "[]")).toHaveLength(1);
  });

  it("does not add the same movie twice", () => {
    const { result } = renderHook(() => useWatchlist(), { wrapper: WatchlistProvider });

    act(() => {
      result.current.add(MOVIE);
      result.current.add(MOVIE);
    });

    expect(result.current.items).toHaveLength(1);
  });

  it("removes a movie", () => {
    const { result } = renderHook(() => useWatchlist(), { wrapper: WatchlistProvider });

    act(() => result.current.add(MOVIE));
    act(() => result.current.remove(1));

    expect(result.current.isWatchlisted(1)).toBe(false);
    expect(result.current.items).toHaveLength(0);
  });

  it("toggle adds when absent and removes when present", () => {
    const { result } = renderHook(() => useWatchlist(), { wrapper: WatchlistProvider });

    act(() => result.current.toggle(MOVIE));
    expect(result.current.isWatchlisted(1)).toBe(true);

    act(() => result.current.toggle(MOVIE));
    expect(result.current.isWatchlisted(1)).toBe(false);
  });
});
