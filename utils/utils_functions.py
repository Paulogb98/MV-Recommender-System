import pandas as pd

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


def concat_ratings_df(unique_movies_list, movies_df, ratings_df):
    """
    Concatena as avaliações dos filmes escolhidos pelo usuário com a tabela de avaliações existentes. 
    Cada filme selecionado recebe uma avaliação máxima (5.0) associada a um usuário fictício identificado como `-1`.

    Argumentos:
        unique_movies_list (list): Lista de títulos de filmes escolhidos pelo usuário.
        movies_df (pandas.DataFrame): DataFrame contendo informações sobre os filmes, 
            incluindo as colunas 'title' e 'movieId'.
        ratings_df (pandas.DataFrame): DataFrame contendo as avaliações existentes, 
            incluindo as colunas 'userId', 'movieId' e 'rating'.

    Retorna:
        pandas.DataFrame: Um novo DataFrame contendo as avaliações originais e as adicionadas pelos filmes escolhidos.
    """
    # Criar um dicionário de títulos e respectivos movieId
    movie_titles_dict = dict(zip(movies_df['title'], movies_df['movieId']))

    # Função para localizar o movieId com base no título do filme
    def find_movie_id(title):
        return movie_titles_dict.get(title, None)

    # Criar uma lista com os movieIds encontrados para os filmes
    movie_ids = [find_movie_id(title) for title in unique_movies_list]

    # Criar um DataFrame com userId = -1, movieId e rating = 5.0
    ratings_data = []
    for movie_id in movie_ids:
        ratings_data.append({'userId': -1, 'movieId': movie_id, 'rating': 5.0})
    
    ratings_user = pd.DataFrame(ratings_data)
    
    # Concatenar os DataFrames
    ratings_concatenated = pd.concat([ratings_df, ratings_user], axis=0, ignore_index=True)
    
    return ratings_concatenated


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
    # Ajustar tipos das colunas
    movies = movies.astype({'movieId': int, 'title': str})
    links_tmdb['tmdbId'] = links_tmdb['tmdbId'].astype('Int64')  # Int64 Pandas para NaN
    
    # Selecionar apenas as colunas relevantes
    movies = movies[['movieId', 'title']]
    
    # Mesclar os DataFrames
    df_merged = pd.merge(left=movies, right=links_tmdb, how='inner')
    
    # Selecionar as colunas finais
    df_merged = df_merged[['movieId', 'title', 'tmdbId']]    
    
    # Filtrar as linhas com base nos IDs recomendados
    filtered_df = df_merged[df_merged['movieId'].isin(recommended_movies)]
    
    return filtered_df['tmdbId'].tolist()
