import { useEffect, useRef, useState } from "react";
import { useMovieSearch } from "../../hooks/useMovieSearch";
import { usePoster } from "../../hooks/usePoster";
import type { Movie, MovieFilters } from "../../types";
import { swatchFor } from "../../utils/swatch";
import { SelectedChips } from "./SelectedChips";

interface SearchBoxProps {
  selectedMovies: Movie[];
  onSelect: (movie: Movie) => void;
  onRemove: (movieId: number) => void;
  filters: MovieFilters;
}

const MAX_SELECTED = 3;

function DropdownItem({ movie, onSelect }: { movie: Movie; onSelect: (movie: Movie) => void }) {
  const poster = usePoster(movie.movie_id);

  return (
    <button className="mv-dropdown-item" onClick={() => onSelect(movie)}>
      {poster?.poster_url ? (
        <img className="mv-dropdown-item-thumb" src={poster.poster_url} alt="" />
      ) : (
        <div className="mv-dropdown-item-thumb" style={{ background: swatchFor(movie.movie_id) }} />
      )}
      <div>
        <div className="mv-dropdown-item-title">{movie.title}</div>
        <div className="mv-dropdown-item-meta">
          {movie.year ?? "—"} · {movie.genres[0] ?? "—"}
        </div>
      </div>
    </button>
  );
}

export function SearchBox({ selectedMovies, onSelect, onRemove, filters }: SearchBoxProps) {
  const [query, setQuery] = useState("");
  const [focused, setFocused] = useState(false);
  const wrapRef = useRef<HTMLDivElement>(null);
  const selectedIds = selectedMovies.map((m) => m.movie_id);
  const searchDisabled = selectedMovies.length >= MAX_SELECTED;

  const { results } = useMovieSearch(query, filters, selectedIds);
  const showDropdown = focused && !searchDisabled;

  // Closes the dropdown on an outside click (more robust than onBlur, which fires
  // before the click on a dropdown item gets processed).
  useEffect(() => {
    if (!focused) return;
    const handleOutsideClick = (event: MouseEvent) => {
      if (wrapRef.current && !wrapRef.current.contains(event.target as Node)) {
        setFocused(false);
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    return () => document.removeEventListener("mousedown", handleOutsideClick);
  }, [focused]);

  const handleSelect = (movie: Movie) => {
    onSelect(movie);
    setQuery("");
    setFocused(false);
  };

  return (
    <>
      <div className="mv-search-wrap" ref={wrapRef}>
        <div className={`mv-search-box${focused ? " is-focused" : ""}`}>
          <span className="mv-search-icon">⌕</span>
          <input
            className="mv-search-input"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => setFocused(true)}
            placeholder={selectedMovies.length > 0 ? "Add another movie…" : "E.g. Matrix, Dune, Fight Club…"}
            disabled={searchDisabled}
          />
          {query.length > 0 && (
            <button className="mv-search-clear" onClick={() => setQuery("")}>
              ✕
            </button>
          )}
        </div>

        {showDropdown && (
          <div className="mv-dropdown">
            {results.length > 0 ? (
              results.map((movie) => <DropdownItem key={movie.movie_id} movie={movie} onSelect={handleSelect} />)
            ) : (
              <div className="mv-dropdown-empty">No movies found.</div>
            )}
          </div>
        )}
      </div>

      <SelectedChips movies={selectedMovies} onRemove={onRemove} />
    </>
  );
}
