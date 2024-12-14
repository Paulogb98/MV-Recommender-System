from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import numpy as np

# ---------------------------------------------------------------------
# User-Item Matrix
def create_matrix(df):
    """
    Cria uma matriz esparsa que representa as avaliações dos usuários para os filmes.

    Esta matriz é usada para calcular a similaridade entre filmes com base nas avaliações dos usuários.
    
    Argumentos:
        df (pandas.DataFrame): DataFrame contendo as colunas 'userId', 'movieId' e 'rating'.
    
    Retorna:
        tuple: Contém a matriz esparsa (csr_matrix), os mapeamentos de usuários e filmes para índices e
               os mapeamentos invertidos de índices para IDs de usuários e filmes.
    """
    
    N = len(df['userId'].unique())
    M = len(df['movieId'].unique())
    
    # Mapear IDs para índices
    user_mapper = dict(zip(np.unique(df["userId"]), list(range(N))))
    movie_mapper = dict(zip(np.unique(df["movieId"]), list(range(M))))
    
    # Mapear índices de volta para os IDs
    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["userId"])))
    movie_inv_mapper = dict(zip(list(range(M)), np.unique(df["movieId"])))
    
    user_index = [user_mapper[i] for i in df['userId']]
    movie_index = [movie_mapper[i] for i in df['movieId']]

    X = csr_matrix((df["rating"], (movie_index, user_index)), shape=(M, N))
    
    return X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper


# ---------------------------------------------------------------------
# Find similar movies using KNN
def find_similar_movies(movie_id, X, movie_mapper, movie_inv_mapper, k, metric='cosine', show_distance=False):
    """
    Encontra filmes semelhantes ao filme fornecido usando o algoritmo KNN (K-Nearest Neighbors).

    Argumentos:
        movie_id (int): ID do filme para o qual encontrar filmes semelhantes.
        X (csr_matrix): Matriz esparsa contendo as avaliações dos usuários para os filmes.
        movie_mapper (dict): Mapeamento de IDs de filmes para índices na matriz.
        movie_inv_mapper (dict): Mapeamento invertido de índices para IDs de filmes.
        k (int): Número de filmes semelhantes a serem retornados.
        metric (str, opcional): Métrica de distância para calcular a similaridade, padrão é 'cosine'.
        show_distance (bool, opcional): Se True, retorna também a distância entre os filmes, padrão é False.

    Retorna:
        list: Lista de IDs de filmes semelhantes ao filme fornecido.
    """
    
    neighbour_ids = []
    
    movie_ind = movie_mapper[movie_id]
    movie_vec = X[movie_ind]
    k += 1  # Incluir o próprio filme na lista de vizinhos
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)
    movie_vec = movie_vec.reshape(1, -1)
    neighbour = kNN.kneighbors(movie_vec, return_distance=show_distance)
    
    for i in range(0, k):
        n = neighbour.item(i)
        neighbour_ids.append(movie_inv_mapper[n])
    
    neighbour_ids.pop(0)  # Remover o filme original da lista
    return neighbour_ids


# ---------------------------------------------------------------------
# Create a function to recommend the movies based on the user preferences.
def recommend_movies_for_user(user_id, X, user_mapper, movie_mapper, movie_inv_mapper, ratings_user, k=10):
    """
    Recomenda filmes para um usuário com base nas avaliações de outros filmes e preferências anteriores.

    A função recomenda filmes semelhantes aos filmes avaliados positivamente pelo usuário e remove
    os filmes já escolhidos pelo próprio usuário.

    Argumentos:
        user_id (int): ID do usuário para o qual recomendar filmes.
        X (csr_matrix): Matriz esparsa contendo as avaliações dos usuários para os filmes.
        user_mapper (dict): Mapeamento de IDs de usuários para índices na matriz.
        movie_mapper (dict): Mapeamento de IDs de filmes para índices na matriz.
        movie_inv_mapper (dict): Mapeamento invertido de índices para IDs de filmes.
        ratings_user (pandas.DataFrame): DataFrame contendo as avaliações dos usuários.
        k (int, opcional): Número de filmes recomendados a serem retornados, padrão é 10.
    
    Retorna:
        list: Lista de IDs de filmes recomendados para o usuário, sem incluir os filmes que ele já escolheu.
    """
    # Filtra os filmes avaliados pelo usuário
    df1 = ratings_user[ratings_user['userId'] == user_id]

    # Ordena os filmes pelas avaliações e seleciona os top 3
    top_movies = df1.sort_values(by='rating', ascending=False).head(3)

    # Obtém os ids dos filmes favoritos (1 a 3 filmes)
    top_movie_ids = top_movies['movieId'].tolist()

    # Agora encontra filmes semelhantes aos filmes favoritos
    similar_ids = []
    for movie_id in top_movie_ids:
        similar_ids += find_similar_movies(movie_id, X, movie_mapper, movie_inv_mapper, k)

    # Remove duplicatas da lista de filmes semelhantes
    similar_ids = list(set(similar_ids))
    
    # Remove os filmes escolhidos pelo usuário para garantir que eles não sejam recomendados novamente
    similar_ids = [movie_id for movie_id in similar_ids if movie_id not in top_movie_ids]
        
    return similar_ids
