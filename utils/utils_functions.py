import pandas as pd
import joblib
import requests
from scipy.sparse import csr_matrix


# ---------------------------------------------------------------
def movies_list(movies):
    """
    Gera uma lista única de títulos de filmes disponíveis para o usuário selecionar em um dropdown.

    Argumentos:
        movies (pandas.DataFrame): DataFrame contendo informações sobre os filmes, 
            incluindo uma coluna 'title' com os títulos dos filmes.

    Retorna:
        list: Lista de títulos únicos dos filmes disponíveis no DataFrame.
    """
    return movies['title'].unique().tolist()


# ---------------------------------------------------------------
def search_tmdbId(recommended_movies, movies, links_tmdb):
    """
    Localiza os IDs do TMDB para os filmes recomendados, permitindo buscar informações como pôsteres e metadados.

    Argumentos:
        recommended_movies (list): Lista de IDs dos filmes recomendados pelo modelo.
        movies (pandas.DataFrame): DataFrame contendo informações sobre os filmes, 
            incluindo as colunas 'movieId' e 'title'.
        links_tmdb (pandas.DataFrame): DataFrame contendo a correspondência entre 'movieId' e 'tmdbId' (ID do TMDB).

    Retorna:
        list: Lista de IDs do TMDB correspondentes aos filmes recomendados.
    """
    movies = movies.astype({'movieId': int, 'title': str})
    links_tmdb['tmdbId'] = links_tmdb['tmdbId'].astype('Int64')  # Int64 Pandas para NaN
    df_merged = pd.merge(left=movies, right=links_tmdb, how='inner')
    df_merged = df_merged[['movieId', 'title', 'tmdbId']]
    filtered_df = df_merged[df_merged['movieId'].isin(recommended_movies)]
    return filtered_df['tmdbId'].tolist()


# ---------------------------------------------------------------
def recommend_movies_item_item_loaded(selected_titles: list, movies_df, n_recommendations=5):
    """
    Recomenda filmes com base nos títulos selecionados pelo usuário utilizando um modelo KNN previamente treinado.

    Esta função carrega o modelo KNN e os mapeamentos salvos em disco (.pkl) e realiza 
    a recomendação de filmes similares aos selecionados. Retorna uma lista de IDs dos filmes recomendados.

    Argumentos:
        selected_titles (list): Lista de títulos de filmes escolhidos pelo usuário.
        movies_df (pandas.DataFrame): DataFrame contendo informações sobre os filmes,
            incluindo as colunas 'movieId' e 'title'.
        n_recommendations (int, opcional): Número máximo de recomendações a retornar. Default é 5.

    Retorna:
        list: Lista de IDs de filmes recomendados pelo modelo KNN.
    """
    import joblib
    from scipy.sparse import csr_matrix

    # Carregar modelo KNN e mapeamentos salvos em disco
    knn_model = joblib.load("recommender/models/knn_model.pkl")
    mappers = joblib.load("recommender/models/mappers.pkl")
    movie_mapper = mappers["movie_mapper"]
    movie_inv_mapper = mappers["movie_inv_mapper"]

    # Mapear título -> movieId usando o DataFrame passado
    title_to_id = dict(zip(movies_df['title'], movies_df['movieId']))
    selected_ids = [title_to_id[t] for t in selected_titles if t in title_to_id]

    # Obter índices correspondentes no modelo KNN
    selected_indices = [movie_mapper[mid] for mid in selected_ids if mid in movie_mapper]

    # Conjunto para armazenar recomendações únicas
    recommendations = set()
    for idx in selected_indices:
        distances, indices = knn_model.kneighbors(csr_matrix(knn_model._fit_X[idx]), n_neighbors=n_recommendations+1)
        similar_indices = indices.flatten()[1:]  # Ignora o próprio filme
        for sim_idx in similar_indices:
            recommendations.add(movie_inv_mapper[sim_idx])

    return list(recommendations)[:n_recommendations]
