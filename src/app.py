import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.utils_functions import (
    movies_list,
    search_tmdbId,
    recommend_movies_item_item_loaded
)
from dotenv import load_dotenv
import streamlit as st
import requests
import pandas as pd


# ---------------------------------------------------------------
def configure_sidebar() -> tuple:
    """Configura e exibe os elementos da barra lateral."""
    if 'num_filters' not in st.session_state:
        st.session_state.num_filters = 1
    if 'prompts' not in st.session_state:
        st.session_state.prompts = []

    with st.sidebar:
        with st.form("my_form"):
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.image("assets/img/mv-horizontal-logo.png", width=300)

            with st.expander("**Refine sua pesquisa aqui**"):
                num_outputs = st.slider("Número de pôsteres a exibir", value=10, min_value=1, max_value=10)

            if len(st.session_state.prompts) == 0:
                st.session_state.prompts.append("Action")  # Valor padrão

            st.session_state.prompts[0] = st.selectbox(
                "Selecione um filme", 
                movies_list(movies),
                help="Comece a digitar para procurar um filme",
                key="movie_0"
            )

            for i in range(1, st.session_state.num_filters):
                st.session_state.prompts.append(
                    st.selectbox(
                        "Selecione um filme", 
                        movies_list(movies),
                        help="Comece a digitar para procurar um filme",
                        key=f"movie_{i}"
                    )
                )

            if st.session_state.num_filters < 3:
                add_filter = st.form_submit_button("Adicionar filtro")
                if add_filter:
                    st.session_state.num_filters += 1

            st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Enviar", type="primary", use_container_width=True)

    return submitted, num_outputs, st.session_state.prompts

# ---------------------------------------------------------------
def get_movie_posters(movie_ids: list, num_outputs: int) -> list:
    """Busca pôsteres e títulos de filmes na API TMDB com base nos IDs dos filmes."""
    movie_data = []
    for movie_id in movie_ids[:num_outputs]:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}'
        params = {'api_key': TMDB_API_KEY}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            title = data.get('title', 'Título Desconhecido')
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
    num_items = num_outputs
    if submitted:
        st.session_state.prompts = [st.session_state[f"movie_{i}"] for i in range(st.session_state.num_filters)]
        
        # Gera recomendações diretamente do modelo .pkl
        recommended_movies = recommend_movies_item_item_loaded(
            st.session_state.prompts,  # títulos selecionados
            movies,                     # passa o DataFrame
            n_recommendations=num_items
        )

        status_placeholder = st.empty()
        with status_placeholder.container():
            st.status('🔍 Buscando pôsteres de filmes...', expanded=True)
            st.write("⚙️ Procurando pôsteres...")
            st.write("🙆‍♀️ Faça uma pausa enquanto isso")

        movie_posters = get_movie_posters(search_tmdbId(recommended_movies, movies, links_tmdb), num_items)
        status_placeholder.empty()

        if movie_posters:
            with gallery_placeholder.container():
                cols = st.columns(5, gap="medium")
                for i in range(0, num_items, 5):
                    row_cols = cols
                    for j in range(5):
                        if i + j < num_items:
                            with row_cols[j]:
                                poster_data = movie_posters[i + j]
                                st.image(poster_data["poster_url"], caption=poster_data["title"], use_container_width=True)
                                st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    else:
        with gallery_placeholder.container():
            cols = st.columns(5, gap="medium")
            for i in range(0, num_items, 5):
                row_cols = cols
                for j in range(5):
                    if i + j < num_items:
                        with row_cols[j]:
                            st.markdown(
                                f"""
                                <div style="width: 100%; aspect-ratio: 2/3; background-color: #e0e0e0; 
                                            display: flex; justify-content: center; align-items: center;
                                            border-radius: 5px; margin-bottom: 40px;">
                                    <span style="font-size: 18px; color: #888;">Filme {i + j + 1}</span>
                                </div>
                                """, unsafe_allow_html=True
                            )

# ---------------------------------------------------------------
def main():
    submitted, num_outputs, prompts = configure_sidebar()
    main_page(submitted, num_outputs, prompts)

# ---------------------------------------------------------------
# Importa dados
pd.options.display.float_format = '{:,.2f}'.format
links_tmdb = pd.read_csv("data/links.csv")
movies = pd.read_csv("data/movies.csv")

# Configurações de UI
st.set_page_config(page_title="Recomendador de Filmes",
                   page_icon=":film_frames:",
                   layout="wide")
st.markdown("<h1 style='margin-bottom: 30px;'>Recomendações baseadas no seu perfil</h1>", unsafe_allow_html=True)

# Placeholders
gallery_placeholder = st.empty()

# Carrega .env
load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

if __name__ == "__main__":
    main()
