import logo from "../../assets/mv-reel-logo.png";
import { useWatchlist } from "../../context/WatchlistContext";

interface HeaderProps {
  onOpenWatchlist: () => void;
}

export function Header({ onOpenWatchlist }: HeaderProps) {
  const { items } = useWatchlist();

  return (
    <header className="mv-header">
      <div className="mv-logo-wrap">
        <img src={logo} alt="MV Recommendation System" />
      </div>
      <div className="mv-header-actions">
        <button className="mv-icon-btn" onClick={onOpenWatchlist} title="Watchlist">
          ♥ {items.length > 0 ? items.length : ""}
        </button>
      </div>
    </header>
  );
}
