import { useTrending } from "../../hooks/useTrending";
import { MovieCard } from "../ResultsGrid/MovieCard";

export function TrendingSection() {
  const { items, isLoading } = useTrending(10);

  if (isLoading || items.length === 0) return null;

  return (
    <section className="mv-trending-section">
      <h2 className="mv-trending-title">Trending</h2>
      <div className="mv-grid">
        {items.map((movie) => (
          <MovieCard key={movie.movie_id} movie={movie} rating={movie.avg_rating} />
        ))}
      </div>
    </section>
  );
}
