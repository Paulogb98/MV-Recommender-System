import { useState } from "react";
import { Controls } from "./components/Controls/Controls";
import { FilterPanel } from "./components/FilterPanel/FilterPanel";
import { Header } from "./components/Header/Header";
import { Hero } from "./components/Hero/Hero";
import { ResultsGrid } from "./components/ResultsGrid/ResultsGrid";
import { SearchBox } from "./components/SearchBox/SearchBox";
import { TrendingSection } from "./components/Trending/TrendingSection";
import { WatchlistPanel } from "./components/Watchlist/WatchlistPanel";
import { Footer } from "./components/common/Footer";
import { useRecommendations } from "./hooks/useRecommendations";
import type { Movie, MovieFilters } from "./types";

const MAX_SELECTED = 3;

function App() {
  const [selectedMovies, setSelectedMovies] = useState<Movie[]>([]);
  const [filters, setFilters] = useState<MovieFilters>({});
  const [numOutputs, setNumOutputs] = useState(5);
  const [isWatchlistOpen, setWatchlistOpen] = useState(false);

  const { status, results, submit, reset } = useRecommendations();

  const handleSelect = (movie: Movie) => {
    if (selectedMovies.length >= MAX_SELECTED || selectedMovies.some((m) => m.movie_id === movie.movie_id)) return;
    setSelectedMovies((prev) => [...prev, movie]);
  };

  const handleRemove = (movieId: number) => {
    setSelectedMovies((prev) => prev.filter((m) => m.movie_id !== movieId));
  };

  const handleSubmit = () => {
    if (selectedMovies.length === 0 || status === "loading") return;
    submit(
      selectedMovies.map((m) => m.movie_id),
      numOutputs,
    );
  };

  const handleReset = () => {
    reset();
    setSelectedMovies([]);
  };

  return (
    <div className="mv-app">
      <Header onOpenWatchlist={() => setWatchlistOpen(true)} />

      <section className="mv-hero">
        <Hero />
        <SearchBox selectedMovies={selectedMovies} onSelect={handleSelect} onRemove={handleRemove} filters={filters} />
        <FilterPanel filters={filters} onChange={setFilters} />
        <Controls
          numOutputs={numOutputs}
          onNumOutputsChange={setNumOutputs}
          onSubmit={handleSubmit}
          submitDisabled={selectedMovies.length === 0 || status === "loading"}
          isLoading={status === "loading"}
        />
      </section>

      <section className="mv-results-section">
        <ResultsGrid status={status} results={results} onReset={handleReset} />
      </section>

      <TrendingSection />

      <Footer />

      <WatchlistPanel isOpen={isWatchlistOpen} onClose={() => setWatchlistOpen(false)} />
    </div>
  );
}

export default App;
