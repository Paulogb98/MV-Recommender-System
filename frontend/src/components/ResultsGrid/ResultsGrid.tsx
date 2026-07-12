import type { RecommendationStatus } from "../../hooks/useRecommendations";
import type { RecommendationResult } from "../../types";
import { MovieCard } from "./MovieCard";
import { SkeletonCard } from "./SkeletonCard";

interface ResultsGridProps {
  status: RecommendationStatus;
  results: RecommendationResult[];
  onReset: () => void;
}

const SKELETON_SLOTS = Array.from({ length: 5 }, (_, i) => i);

export function ResultsGrid({ status, results, onReset }: ResultsGridProps) {
  if (status === "loading") {
    return (
      <>
        <div className="mv-loading-row">
          <span className="mv-spinner" />
          Computing cosine similarity…
        </div>
        <div className="mv-grid">
          {SKELETON_SLOTS.map((i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      </>
    );
  }

  if (status === "results") {
    return (
      <>
        <div className="mv-results-header">
          <h2 className="mv-results-title">Recommended for you</h2>
          <button className="mv-reset-btn" onClick={onReset}>
            New search
          </button>
        </div>
        <div className="mv-grid">
          {results.map((movie, i) => (
            <MovieCard key={movie.movie_id} movie={movie} rating={movie.avg_rating} delaySeconds={i * 0.05} />
          ))}
        </div>
      </>
    );
  }

  if (status === "error") {
    return <div className="mv-dropdown-empty">Couldn't compute recommendations right now. Please try again.</div>;
  }

  return (
    <div className="mv-grid">
      {SKELETON_SLOTS.map((i) => (
        <div key={i} className="mv-idle-placeholder">
          Select movies above
        </div>
      ))}
    </div>
  );
}
