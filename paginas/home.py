import streamlit as st
from common import PROJETOS, links_projeto

st.title("📊 Portfólio de Dados · Emmanuel VRM")
st.markdown(
    "Cientista de dados, engenheiro de dados e de ML. Aqui cada projeto roda como **aplicação de verdade**: "
    "escolha um projeto abaixo (ou no menu lateral), interaja com o modelo e, se quiser, "
    "abra o notebook original no Colab ou o código no GitHub."
)
st.info("👀 Para recrutadores: leva ~1 minuto por projeto. Cada página tem entrada de dados, resultado e links para o código.")

cols = st.columns(2)
rotas = {"inadimplentes": "paginas/inadimplentes.py", "enem": "paginas/enem.py",
         "depressao": "paginas/depressao.py", "jogos": "paginas/jogos.py"}
for i, (chave, p) in enumerate(PROJETOS.items()):
    with cols[i % 2].container(border=True):
        st.subheader(f"{p['icone']} {p['titulo']}")
        st.write(p["resumo"])
        st.caption(f"**Stack:** {p['stack']}  \n**Habilidades:** {p['habilidades']}")
        st.page_link(rotas[chave], label="Abrir app", icon="▶️")
        links_projeto(chave)

st.divider()
st.markdown(
    "**Perfil:** [GitHub](https://github.com/emmanuelvrm) · [LinkedIn](https://www.linkedin.com/in/emmanuelvrm/)  \n"
    "**Código deste site:** [portfolio-app](https://github.com/emmanuelvrm/portfolio-app)"
)
