import random
import pandas as pd
import streamlit as st
from common import BASE, cabecalho


@st.cache_data
def carregar():
    sj = pd.read_csv(BASE / "data" / "streamer_jogos.csv")
    cat = pd.read_csv(BASE / "data" / "jogos_catalogo.csv")
    cat["storyline"] = cat["storyline"].fillna("")
    return sj, cat


def recomendar(streamer, sj, cat, n=10, semente=None):
    """Perfil de gêneros do streamer (ponderado por VODs) -> jogos dos 2 gêneros líderes ainda não jogados."""
    jogados = sj[sj.user_name == streamer]
    base = cat[cat.game_name.isin(jogados.game_name)].merge(jogados, on="game_name")
    peso = {}
    for _, r in base.iterrows():
        for g in str(r.generos).split("|"):
            if g:
                peso[g] = peso.get(g, 0) + r.vods
    top = [g for g, _ in sorted(peso.items(), key=lambda x: -x[1])[:2]]
    if not top:
        return top, cat.iloc[0:0]
    cand = cat[~cat.game_name.isin(jogados.game_name) & cat.generos.apply(lambda s: any(g in str(s).split("|") for g in top))]
    cand = cand[cand.image_url.notna()]
    return top, cand.sample(min(n, len(cand)), random_state=semente)


cabecalho("jogos")
st.write("Escolha um streamer brasileiro da Twitch (dados de VODs de 2022). O sistema identifica os **gêneros que ele mais transmite** "
         "e sugere jogos desses gêneros que ele ainda não jogou.")
sj, cat = carregar()
n_jogos = sj.groupby("user_name").game_name.nunique()
streamers = sorted(n_jogos[n_jogos >= 3].index)
streamer = st.selectbox(f"Streamer ({len(streamers)} disponíveis — digite para buscar)", streamers,
                        index=streamers.index("gaules") if "gaules" in streamers else 0)
if "semente" not in st.session_state:
    st.session_state.semente = random.randint(0, 10**6)
if st.button("🔀 Outras sugestões"):
    st.session_state.semente = random.randint(0, 10**6)

generos, recs = recomendar(streamer, sj, cat, semente=st.session_state.semente)
if recs.empty:
    st.info("Sem dados suficientes para este streamer.")
else:
    jogados = sj[sj.user_name == streamer].sort_values("vods", ascending=False).head(5).game_name.str.title().tolist()
    st.markdown(f"**Mais joga:** {', '.join(jogados)}  \n**Gêneros líderes:** {' · '.join(generos)}")
    st.subheader("Recomendamos")
    for _, r in recs.iterrows():
        with st.container(border=True):
            a, b = st.columns([3, 1])
            a.markdown(f"#### {str(r.game_name).title()}")
            a.caption(f"Gêneros: {r.generos.replace('|', ', ')}  ·  Transmissões na Twitch: {int(r.streams)}  ·  "
                      f"Avaliação IGDB: {r.rating if pd.notna(r.rating) else 'sem avaliação'}")
            if r.storyline:
                a.write(r.storyline)
            b.image(r.image_url)

with st.expander("Sobre o projeto"):
    st.markdown("Projeto em grupo do curso Tera (Emmanuel, Italo, Kamila e Nilton). Dados: Twitch API + IGDB. "
                "Esta versão corrige o app original (sorteios fora de índice, lista aninhada) e roda de forma estável.")
