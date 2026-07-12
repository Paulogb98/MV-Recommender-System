import { useWatchlist } from "../../context/WatchlistContext";
import { usePoster } from "../../hooks/usePoster";
import type { Movie } from "../../types";

interface WatchlistPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

function WatchlistRow({ movie, onRemove }: { movie: Movie; onRemove: () => void }) {
  const poster = usePoster(movie.movie_id);

  return (
    <div className="mv-watchlist-item">
      {poster?.poster_url ? (
        <img className="mv-watchlist-item-thumb" src={poster.poster_url} alt={movie.title} />
      ) : (
        <div className="mv-watchlist-item-thumb" style={{ background: "var(--mv-chip-bg)" }} />
      )}
      <div className="mv-watchlist-item-title">{movie.title}</div>
      <button className="mv-chip-remove" onClick={onRemove}>
        ✕
      </button>
    </div>
  );
}

export function WatchlistPanel({ isOpen, onClose }: WatchlistPanelProps) {
  const { items, remove } = useWatchlist();

  if (!isOpen) return null;

  return (
    <>
      <div className="mv-watchlist-overlay" onClick={onClose} />
      <div className="mv-watchlist-drawer">
        <div className="mv-watchlist-header">
          <h3 className="mv-watchlist-title">Your watchlist</h3>
          <button className="mv-icon-btn" onClick={onClose}>
            ✕
          </button>
        </div>
        {items.length === 0 ? (
          <div className="mv-watchlist-empty">No movies saved yet.</div>
        ) : (
          items.map((movie) => (
            <WatchlistRow key={movie.movie_id} movie={movie} onRemove={() => remove(movie.movie_id)} />
          ))
        )}
      </div>
    </>
  );
}
