export interface Movie {
  movie_id: number;
  title: string;
  year: number | null;
  genres: string[];
  tmdb_id: number | null;
  avg_rating: number | null;
  n_ratings: number;
}

export interface RecommendationResult extends Movie {
  score: number;
}

export interface TrendingItem extends Movie {
  trending_score: number;
}

export interface Poster {
  tmdb_id: number;
  title: string | null;
  poster_url: string | null;
}

export interface MovieFilters {
  genre?: string;
  yearMin?: number;
  yearMax?: number;
  minRating?: number;
}
