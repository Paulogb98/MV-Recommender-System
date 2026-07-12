import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { SearchBox } from "../SearchBox";

const MOVIE = {
  movie_id: 1,
  title: "Matrix",
  year: 1999,
  genres: ["Sci-Fi"],
  tmdb_id: 603,
  avg_rating: 4.1,
  n_ratings: 1000,
};

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("SearchBox", () => {
  it("shows matching movies in the dropdown and selects one", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({ ok: true, json: async () => [MOVIE] }),
    );

    const onSelect = vi.fn();
    const user = userEvent.setup();

    render(<SearchBox selectedMovies={[]} onSelect={onSelect} onRemove={vi.fn()} filters={{}} />);

    const input = screen.getByPlaceholderText(/E\.g\. Matrix/);
    await user.click(input);
    await user.type(input, "matrix");

    const item = await waitFor(() => screen.getByText("Matrix"), { timeout: 2000 });
    await user.pointer({ target: item, keys: "[MouseLeft]" });

    expect(onSelect).toHaveBeenCalledWith(MOVIE);
  });

  it("disables the input once 3 movies are selected", () => {
    const threeMovies = [1, 2, 3].map((id) => ({ ...MOVIE, movie_id: id }));
    render(<SearchBox selectedMovies={threeMovies} onSelect={vi.fn()} onRemove={vi.fn()} filters={{}} />);

    expect(screen.getByPlaceholderText(/Add another movie/)).toBeDisabled();
  });
});
