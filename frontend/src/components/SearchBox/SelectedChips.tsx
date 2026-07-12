import { usePoster } from "../../hooks/usePoster";
import type { Movie } from "../../types";
import { swatchFor } from "../../utils/swatch";

interface SelectedChipsProps {
  movies: Movie[];
  onRemove: (movieId: number) => void;
}

function Chip({ movie, onRemove }: { movie: Movie; onRemove: () => void }) {
  const poster = usePoster(movie.movie_id);

  return (
    <div className="mv-chip">
      {poster?.poster_url ? (
        <img className="mv-chip-thumb" src={poster.poster_url} alt="" />
      ) : (
        <div className="mv-chip-thumb" style={{ background: swatchFor(movie.movie_id) }} />
      )}
      <span className="mv-chip-label">{movie.title}</span>
      <button className="mv-chip-remove" onClick={onRemove}>
        ✕
      </button>
    </div>
  );
}

export function SelectedChips({ movies, onRemove }: SelectedChipsProps) {
  if (movies.length === 0) return null;

  return (
    <div className="mv-chips-row">
      {movies.map((movie) => (
        <Chip key={movie.movie_id} movie={movie} onRemove={() => onRemove(movie.movie_id)} />
      ))}
    </div>
  );
}
