import requests
import streamlit as st

st.set_page_config(page_title="Letras de Músicas", layout="centered")

def carregar_css():
    with open("style.css", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

carregar_css()


def buscar_letra(banda, musica):
    endpoint = f"https://api.lyrics.ovh/v1/{banda}/{musica}"
    response = requests.get(endpoint)

    if response.status_code == 200:
        return response.json()["lyrics"]

    return ""


def album(banda, musica):
    endpoint = f'https://api.deezer.com/search?q=artist:"{banda}" track:"{musica}"'
    response = requests.get(endpoint)

    if response.status_code == 200:
        dados = response.json()

        if len(dados["data"]) > 0:
            return dados["data"][0]["album"]["cover_xl"]

    return None


# ---------------- Título ----------------

st.markdown("<h1 style='text-align:center;'>Letras de Músicas</h1>", unsafe_allow_html=True)

# ---------------- Formulário ----------------

banda = st.text_input("Digite o nome da banda/artista")
musica = st.text_input("Digite o nome da música")

# ---------------- Botão Centralizado ----------------

col1, col2, col3 = st.columns([2, 1, 2])

with col2:
    pesquisar = st.button("PESQUISAR", use_container_width=True)

# ---------------- Resultado ----------------

if pesquisar:

    capa = album(banda, musica)

    if capa:

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.image(capa, width=250)
            st.markdown(
                f"<h3 style='text-align:left'>{banda.title()} - {musica.title()}</h3>",
                unsafe_allow_html=True
            )

    else:
        st.warning("Capa do álbum não encontrada.")

    letra = buscar_letra(banda, musica)

    if letra:
        st.success("Letra encontrada com sucesso!")
        st.markdown(
            f"<div style='text-align:center; white-space:pre-wrap;'>{letra}</div>",
            unsafe_allow_html=True
        )
    else:
        st.error("Letra não encontrada.")