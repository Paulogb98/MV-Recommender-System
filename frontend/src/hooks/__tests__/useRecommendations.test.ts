import { act, renderHook, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { useRecommendations } from "../useRecommendations";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("useRecommendations", () => {
  it("goes idle -> loading -> results on success", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => [{ movie_id: 1, title: "Matrix", year: 1999, genres: [], tmdb_id: 603, avg_rating: 4.1, n_ratings: 100, score: 0.9 }],
    });
    vi.stubGlobal("fetch", fetchMock);

    const { result } = renderHook(() => useRecommendations());
    expect(result.current.status).toBe("idle");

    act(() => {
      void result.current.submit([1, 2], 5);
    });
    expect(result.current.status).toBe("loading");

    await waitFor(() => expect(result.current.status).toBe("results"));
    expect(result.current.results).toHaveLength(1);
    expect(result.current.results[0].title).toBe("Matrix");
  });

  it("goes to error state when the request fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 500, json: async () => ({}) }));

    const { result } = renderHook(() => useRecommendations());
    await act(async () => {
      await result.current.submit([1], 5);
    });

    expect(result.current.status).toBe("error");
    expect(result.current.results).toEqual([]);
  });

  it("reset() clears results back to idle", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => [{ movie_id: 1, title: "Matrix", year: 1999, genres: [], tmdb_id: 603, avg_rating: 4.1, n_ratings: 100, score: 0.9 }],
      }),
    );

    const { result } = renderHook(() => useRecommendations());
    await act(async () => {
      await result.current.submit([1], 5);
    });
    expect(result.current.status).toBe("results");

    act(() => result.current.reset());
    expect(result.current.status).toBe("idle");
    expect(result.current.results).toEqual([]);
  });
});
