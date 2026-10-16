"""Metadados e utilitários compartilhados pelas páginas do portfólio."""
from pathlib import Path
import streamlit as st

BASE = Path(__file__).parent
GH = "https://github.com/emmanuelvrm"

PROJETOS = {
    "inadimplentes": {
        "titulo": "Análise de Inadimplentes",
        "icone": "💳",
        "resumo": "Análise exploratória do que está por trás da inadimplência de clientes de uma instituição financeira.",
        "stack": "Python · pandas · seaborn · SciPy · Plotly",
        "habilidades": "EDA, limpeza de dados, testes estatísticos, storytelling com dados",
        "repo": f"{GH}/analise-inadimplentes",
        "colab": "https://colab.research.google.com/github/emmanuelvrm/analise-inadimplentes/blob/main/notebooks/Analise_Inadimplentes.ipynb",
    },
    "enem": {
        "titulo": "Previsão da nota do ENEM 2021",
        "icone": "🎓",
        "resumo": "Regressão (LightGBM via PyCaret) que estima a média do ENEM a partir de dados socioeconômicos.",
        "stack": "Python · PyCaret · LightGBM · statsmodels",
        "habilidades": "Feature engineering, AutoML, regressão, deploy de modelo",
        "repo": f"{GH}/desempenho-enem-2021",
        "colab": "https://colab.research.google.com/github/emmanuelvrm/desempenho-enem-2021/blob/main/notebooks/Desempenho_ENEM.ipynb",
    },
    "depressao": {
        "titulo": "Depressão e hábitos saudáveis",
        "icone": "🧠",
        "resumo": "Modelo (Extra Trees) que infere sintomas depressivos (PHQ-9) a partir de dieta e atividade física (NHANES).",
        "stack": "Python · PyCaret · scikit-learn",
        "habilidades": "Classificação desbalanceada, testes de hipótese, métricas (recall/AUC), ética em saúde",
        "repo": f"{GH}/inferencia-depressao-habitos-saudaveis",
        "colab": "https://colab.research.google.com/github/emmanuelvrm/inferencia-depressao-habitos-saudaveis/blob/main/notebooks/Inferencia_Depressao_e_Habitos_Saudaveis.ipynb",
    },
    "jogos": {
        "titulo": "Recomendador de jogos (Twitch)",
        "icone": "🎮",
        "resumo": "Sistema de recomendação baseado em conteúdo: sugere jogos a partir dos gêneros que cada streamer mais transmite.",
        "stack": "Python · pandas · Streamlit · APIs Twitch e IGDB",
        "habilidades": "Coleta via API, sistemas de recomendação, engenharia de dados, app web (projeto em grupo – Tera)",
        "repo": f"{GH}/recomendacao-jogos-twitch",
        "colab": "https://colab.research.google.com/github/emmanuelvrm/recomendacao-jogos-twitch/blob/main/notebooks/03_modelagem.ipynb",
    },
}


def links_projeto(chave: str):
    p = PROJETOS[chave]
    c1, c2 = st.columns(2)
    c1.link_button("📓 Abrir no Colab", p["colab"], use_container_width=True)
    c2.link_button("💻 Código no GitHub", p["repo"], use_container_width=True)


def cabecalho(chave: str):
    p = PROJETOS[chave]
    st.title(f"{p['icone']} {p['titulo']}")
    st.caption(f"{p['resumo']}  \n**Stack:** {p['stack']}")
    links_projeto(chave)
    st.divider()
