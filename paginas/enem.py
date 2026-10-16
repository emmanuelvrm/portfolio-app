import json
import pandas as pd
import streamlit as st
from pycaret.regression import load_model
from common import BASE, cabecalho


@st.cache_resource(show_spinner="Carregando modelo...")
def modelo():
    return load_model(str(BASE / "model" / "previsao_enem"), verbose=False)


@st.cache_data
def categorias():
    return json.loads((BASE / "data" / "enem_cats.json").read_text(encoding="utf-8"))


cabecalho("enem")
st.write("Informe o perfil socioeconômico e o modelo estima a **média das notas do ENEM 2021**.")
cats = categorias()
ordem_idade = ["Menor de 17 anos", "17 anos", "18 anos", "19 anos", "20 anos", "21 anos", "22 anos", "23 anos",
               "24 anos", "25 anos", "Entre 26 e 30 anos", "Entre 31 e 35 anos", "Entre 36 e 40 anos", "Maior de 41"]
SN = ["Sim.", "Não."]

with st.form("enem"):
    a, b, c = st.columns(3)
    idade = a.selectbox("Faixa etária", ordem_idade, index=ordem_idade.index("18 anos"))
    sexo = b.selectbox("Sexo", ["Feminino", "Masculino"])
    renda = c.number_input("Renda mensal da família (R$)", 0, 50000, 3000, step=100)
    pai = st.selectbox("Escolaridade do pai", sorted(cats["Até que série seu pai estudou?"]))
    mae = st.selectbox("Escolaridade da mãe", sorted(cats["Até que série sua mãe estudou?"]))
    op = st.selectbox("Ocupação do pai", sorted(cats["Ocupação mais próxima da ocupação do seu pai"]))
    om = st.selectbox("Ocupação da mãe", sorted(cats["Ocupação mais próxima da ocupação da sua mãe"]))
    st.markdown("**Bens e serviços na residência**")
    itens = {
        "Empregado(a) doméstico(a)": ("Empregado(a) doméstico(a) na residência", "Não."),
        "Carro": ("Carro na residência", "Sim."),
        "Geladeira": ("Geladeira na residência", "Sim."),
        "Freezer": ("Freezer na residência", "Não."),
        "Máquina de lavar roupa": ("Máquina de lavar roupa na residência", "Sim."),
        "Máquina de secar roupa": ("Máquina de secar roupa na residência", "Não."),
        "Micro-ondas": ("Forno micro-ondas na residência", "Sim."),
        "Máquina de lavar louça": ("Máquina de lavar louça na residência", "Não."),
        "Aspirador de pó": ("Aspirador de pó na residência", "Não."),
        "Aparelho de DVD": ("Aparelho de DVD na residência", "Sim."),
        "TV por assinatura": ("TV por assinatura na residência", "Não."),
        "Telefone fixo": ("Telefone fixo na residência", "Não."),
        "Computador": ("Computador na residência", "Sim."),
        "Internet": ("Acesso à Internet na residência", "Sim."),
    }
    cols = st.columns(3)
    resp = {}
    for i, (rotulo, (col, padrao)) in enumerate(itens.items()):
        resp[col] = cols[i % 3].radio(rotulo, SN, index=SN.index(padrao), horizontal=True)
    ok = st.form_submit_button("Estimar nota", type="primary")

if ok:
    dados = pd.DataFrame({
        "TP_FAIXA_ETARIA": [idade], "TP_SEXO": [sexo],
        "Até que série seu pai estudou?": [pai], "Até que série sua mãe estudou?": [mae],
        "Ocupação mais próxima da ocupação do seu pai": [op],
        "Ocupação mais próxima da ocupação da sua mãe": [om],
        **{k: [v] for k, v in resp.items()}, "Renda mensal num": [renda],
    })
    nota = float(modelo().predict(dados)[0])
    st.metric("Média estimada no ENEM", f"{nota:.1f} pontos")
    st.progress(min(max(nota / 1000, 0.0), 1.0))

with st.expander("Como funciona / limitações"):
    st.markdown(
        "- Pipeline PyCaret (LightGBM) treinado com microdados do ENEM 2021 e variáveis socioeconômicas.\n"
        "- É uma **estimativa estatística** de portfólio: reflete desigualdades presentes nos dados, não o potencial de uma pessoa.\n"
        "- Os modelos foram salvos em 2023 e por isso este app fixa versões antigas de pandas/scikit-learn."
    )
