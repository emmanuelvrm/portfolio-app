import streamlit as st

st.set_page_config(page_title="Emmanuel VRM · Portfólio de Dados", page_icon="📊", layout="wide")

paginas = [
    st.Page("paginas/home.py", title="Início", icon="🏠", default=True),
    st.Page("paginas/enem.py", title="ENEM 2021", icon="🎓", url_path="enem"),
    st.Page("paginas/depressao.py", title="Depressão e hábitos", icon="🧠", url_path="depressao"),
    st.Page("paginas/inadimplentes.py", title="Inadimplentes", icon="💳", url_path="inadimplentes"),
    st.Page("paginas/jogos.py", title="Recomendador de jogos", icon="🎮", url_path="jogos"),
]
st.navigation(paginas).run()

with st.sidebar:
    st.markdown("---")
    st.markdown("**Emmanuel VRM**  \n[GitHub](https://github.com/emmanuelvrm) · [LinkedIn](https://www.linkedin.com/in/emmanuelvrm/)")
