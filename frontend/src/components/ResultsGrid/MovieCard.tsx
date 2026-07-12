import { useWatchlist } from "../../context/WatchlistContext";
import { usePoster } from "../../hooks/usePoster";
import type { Movie } from "../../types";
import { swatchFor } from "../../utils/swatch";

interface MovieCardProps {
  movie: Movie;
  rating?: number | null;
  delaySeconds?: number;
}

export function MovieCard({ movie, rating, delaySeconds = 0 }: MovieCardProps) {
  const poster = usePoster(movie.movie_id);
  const { isWatchlisted, toggle } = useWatchlist();
  const active = isWatchlisted(movie.movie_id);
  const displayRating = rating ?? movie.avg_rating;

  return (
    <div className="mv-card" style={{ animationDelay: `${delaySeconds}s` }}>
      <div
        className="mv-card-poster-wrap"
        style={poster?.poster_url ? undefined : { background: swatchFor(movie.movie_id) }}
      >
        {poster?.poster_url && (
          <img className="mv-card-poster-img" src={poster.poster_url} alt={movie.title} loading="lazy" />
        )}
        {displayRating != null && <div className="mv-card-badge">★ {displayRating.toFixed(1)}</div>}
        <button
          className={`mv-card-watchlist-btn${active ? " is-active" : ""}`}
          onClick={(e) => {
            e.stopPropagation();
            toggle(movie);
          }}
          title={active ? "Remove from watchlist" : "Add to watchlist"}
        >
          {active ? "✓" : "+"}
        </button>
        <div className="mv-card-overlay">
          <div className="mv-card-overlay-title">{movie.title}</div>
          <div className="mv-card-overlay-meta">
            {movie.year ?? "—"} · {movie.genres[0] ?? "—"}
          </div>
        </div>
      </div>
    </div>
  );
}
