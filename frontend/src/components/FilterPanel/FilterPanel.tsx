import { useState } from "react";
import type { MovieFilters } from "../../types";

const GENRES = [
  "Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary", "Drama",
  "Fantasy", "Film-Noir", "Horror", "IMAX", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western",
];

interface FilterPanelProps {
  filters: MovieFilters;
  onChange: (filters: MovieFilters) => void;
}

export function FilterPanel({ filters, onChange }: FilterPanelProps) {
  const [open, setOpen] = useState(false);

  return (
    <div>
      <button className="mv-filter-toggle" onClick={() => setOpen((o) => !o)}>
        {open ? "Hide filters" : "Refine by genre, year, or rating"}
      </button>

      {open && (
        <div className="mv-filter-panel">
          <label className="mv-filter-field">
            Genre
            <select
              value={filters.genre ?? ""}
              onChange={(e) => onChange({ ...filters, genre: e.target.value || undefined })}
            >
              <option value="">All</option>
              {GENRES.map((genre) => (
                <option key={genre} value={genre}>
                  {genre}
                </option>
              ))}
            </select>
          </label>

          <label className="mv-filter-field">
            Year
            <div className="mv-filter-year-range">
              <input
                type="number"
                placeholder="From"
                value={filters.yearMin ?? ""}
                onChange={(e) =>
                  onChange({ ...filters, yearMin: e.target.value ? Number(e.target.value) : undefined })
                }
              />
              <input
                type="number"
                placeholder="To"
                value={filters.yearMax ?? ""}
                onChange={(e) =>
                  onChange({ ...filters, yearMax: e.target.value ? Number(e.target.value) : undefined })
                }
              />
            </div>
          </label>

          <label className="mv-filter-field">
            Minimum rating
            <input
              type="number"
              min={0}
              max={5}
              step={0.5}
              placeholder="E.g. 3.5"
              value={filters.minRating ?? ""}
              onChange={(e) =>
                onChange({ ...filters, minRating: e.target.value ? Number(e.target.value) : undefined })
              }
            />
          </label>
        </div>
      )}
    </div>
  );
}
