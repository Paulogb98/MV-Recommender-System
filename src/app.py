import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.utils_functions import movies_list, search_tmdbId, concat_ratings_df
from recommender.model import create_matrix, recommend_movies_for_user
from dotenv import load_dotenv
import streamlit as st
import requests
import pandas as pd


# ---------------------------------------------------------------
def configure_sidebar() -> None:
    """
    Configura e exibe os elementos da barra lateral.
    """
    # Inicializa o estado da sessão se ainda não estiver presente
    if 'num_filters' not in st.session_state:
        st.session_state.num_filters = 1  # Começa com 1 dropdown
    if 'prompts' not in st.session_state:
        st.session_state.prompts = []  # Não há valor fixo, começa vazio

    with st.sidebar:
        with st.form("my_form"):
            col1, col2, col3 = st.columns([1, 2, 1])  # Ajuste as proporções conforme necessário
            with col2:
                st.image("assets/img/mv-horizontal-logo.png", width=300)
            with st.expander("**Refine sua pesquisa aqui**"):
                # Configurações avançadas (para os mais curiosos!)
                num_outputs = st.slider(
                    "Número de pôsteres a exibir", value=10, min_value=1, max_value=10
                )

            # Primeiro dropdown (sempre visível)
            if len(st.session_state.prompts) == 0:
                # Se não houver filmes selecionados, inicia com um valor padrão
                st.session_state.prompts.append("Action")  # Adiciona um prompt padrão
            st.session_state.prompts[0] = st.selectbox(
                "Selecione um filme", 
                movies_list(movies),
                help="Comece a digitar para procurar um filme",
                key="movie_0"  # Chave única para o primeiro dropdown
            )

            # Cria dropdowns adicionais com base no valor de num_filters
            for i in range(1, st.session_state.num_filters):
                st.session_state.prompts.append(
                    st.selectbox(
                        "Selecione um filme", 
                        movies_list(movies),
                        help="Comece a digitar para procurar um filme",
                        key=f"movie_{i}"  # Chave única para cada dropdown adicional
                    )
                )

            # Botão para adicionar um novo filtro, dentro do formulário (antes do botão de envio)
            if st.session_state.num_filters < 3:
                add_filter = st.form_submit_button("Adicionar filtro")
                if add_filter:
                    st.session_state.num_filters += 1
            else:
                # Torna o botão "Adicionar filtro" invisível usando CSS customizado
                st.markdown(
                    """
                    <style>
                    .stButton>button {
                        visibility: hidden;
                    }
                    </style>
                    """, unsafe_allow_html=True
                )

            st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
            
            # Botão para enviar o formulário
            submitted = st.form_submit_button(
                "Enviar", type="primary", use_container_width=True
            )

        # Ícones do GitHub e LinkedIn com links atualizados
        st.markdown(
            """
            <style>
                .social-icons {
                    text-align: center;
                    margin-top: 13vh;
                }
                .social-icons a {
                    text-decoration: none;  /* Remove o sublinhado */
                    margin: 10px;
                }
                .social-icons img {
                    width: 40px;
                    height: 40px;
                    border-radius: 25%;  /* Torna a imagem arredondada */
                }
            </style>
            
            <div class="social-icons">
                <a href="https://github.com/Paulogb98" target="_blank">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub">
                </a>
                <a href="https://br.linkedin.com/in/paulo-goiss" target="_blank">
                    <img src="https://www.pagetraffic.com/blog/wp-content/uploads/2022/09/linkedin-black-logo-icon.png" alt="LinkedIn">
                </a>
            </div>
            """, unsafe_allow_html=True
        )

    return submitted, num_outputs, st.session_state.prompts



# ---------------------------------------------------------------
def get_movie_posters(movie_ids: list, num_outputs: int) -> list:
    """Busca pôsteres e títulos de filmes na API TMDB com base nos IDs dos filmes."""
    movie_data = []

    for movie_id in movie_ids[:num_outputs]:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}'
        params = {
            'api_key': TMDB_API_KEY
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            title = data.get('title', 'Título Desconhecido')  # Valor padrão caso o título esteja ausente
            if poster_path:
                full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                movie_data.append({"poster_url": full_poster_url, "title": title})
        else:
            st.error(f"Falha ao buscar dados para o ID do filme {movie_id}. Código de status: {response.status_code}")

    if not movie_data:
        st.warning("Nenhum pôster encontrado.")
    return movie_data


# ---------------------------------------------------------------
def main_page(submitted: bool, num_outputs: int, prompts: list) -> None:
    """Layout e lógica da página principal para gerar pôsteres de filmes."""
    num_items = num_outputs  # Número de pôsteres a serem exibidos baseado no valor do slider
    if submitted:
        # Reseta o estado dos filmes selecionados para garantir que cada nova rodada comece do zero
        st.session_state.prompts = [st.session_state[f"movie_{i}"] for i in range(st.session_state.num_filters)]
        
        # Usando um conjunto (set) para armazenar valores únicos
        unique_movies = set(st.session_state.prompts)

        ratings_user = concat_ratings_df(unique_movies, movies, ratings)
        
        X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_matrix(ratings)
        user_id = -1  # Substituir pelo ID de usuário desejado
        
        # Retorno do modelo aqui buscando indicações dos filmes escolhidos em movie_ids
        recommended_movies = recommend_movies_for_user(user_id, X, user_mapper, movie_mapper, movie_inv_mapper, ratings_user, k=num_items)

        # Placeholder para exibir status temporário
        status_placeholder = st.empty()
        with status_placeholder.container():
            st.status('🔍 Buscando pôsteres de filmes...', expanded=True)
            st.write("⚙️ Procurando pôsteres...")
            st.write("🙆‍♀️ Faça uma pausa enquanto isso")

        # Busca os pôsteres de filmes usando a API TMDB
        movie_posters = get_movie_posters(search_tmdbId(recommended_movies, movies, links_tmdb), num_items)

        # Após o carregamento, limpa o status
        status_placeholder.empty()

        if movie_posters:
            # Exibe pôsteres de filmes em um layout de grade 2x5
            with gallery_placeholder.container():
                cols = st.columns(5, gap="medium")  # 5 colunas com espaçamento médio
                for i in range(0, num_items, 5):
                    row_cols = cols  # Reutiliza as colunas para cada linha
                    for j in range(5):  # Loop para preencher a linha
                        if i + j < num_items:
                            with row_cols[j]:
                                poster_data = movie_posters[i + j]
                                st.image(poster_data["poster_url"], caption=poster_data["title"], use_container_width=True)
                                # Adiciona margem entre as fileiras
                                st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    else:
        # Renderiza placeholders antes que os resultados sejam exibidos
        with gallery_placeholder.container():
            cols = st.columns(5, gap="medium")  # 5 colunas com espaçamento médio
            for i in range(0, num_items, 5):
                row_cols = cols  # Reutiliza as colunas para cada linha
                for j in range(5):  # Loop para preencher a linha
                    if i + j < num_items:
                        with row_cols[j]:
                            # Imagem placeholder (caixa cinza)
                            st.markdown(
                                """
                                <div style="width: 100%; aspect-ratio: 2/3; background-color: #e0e0e0; 
                                            display: flex; justify-content: center; align-items: center;
                                            border-radius: 5px; margin-bottom: 40px;">
                                    <span style="font-size: 18px; color: #888;">Filme {}</span>
                                </div>
                                """.format(i + j + 1),
                                unsafe_allow_html=True
                            )


# ---------------------------------------------------------------
def main():
    """
    Função principal para executar a aplicação Streamlit.
    """
    submitted, num_outputs, prompts = configure_sidebar()
    main_page(submitted, num_outputs, prompts)


# ---------------------------------------------------------------
# Importa dados e configurações do Pandas
pd.options.display.float_format = '{:,.2f}'.format
links_tmdb = pd.read_csv("data/links.csv")
movies = pd.read_csv("data/movies.csv")
ratings = pd.read_csv("data/ratings.csv")
ratings.drop('timestamp', axis=1, inplace=True)

# Configurações de UI
st.set_page_config(page_title="Recomendador de Filmes",
                   page_icon=":film_frames:",
                   layout="wide")

st.markdown(
    """
    <h1 style="margin-bottom: 30px;">Recomendações baseadas no seu perfil</h1>
    """,
    unsafe_allow_html=True
)

# Placeholders para imagens e galeria
generated_images_placeholder = st.empty()
gallery_placeholder = st.empty()

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Acessa a chave da API TMDB
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

if __name__ == "__main__":
    main()
