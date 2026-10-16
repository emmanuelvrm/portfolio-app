import pandas as pd
import streamlit as st
from pycaret.classification import load_model, predict_model
from common import BASE, cabecalho


@st.cache_resource(show_spinner="Carregando modelo...")
def modelo():
    return load_model(str(BASE / "model" / "previsao_depressao"), verbose=False)


cabecalho("depressao")
st.warning("Projeto educacional. **Não é ferramenta de diagnóstico** e não substitui um profissional de saúde. "
           "Em caso de sofrimento emocional, procure ajuda (no Brasil, CVV: ligue 188).")
st.write("Modelo treinado com dados do NHANES (EUA). Informe os dados e veja a inferência de traços depressivos (PHQ-9).")

with st.form("dep"):
    a, b = st.columns(2)
    genero = a.radio("Gênero (código NHANES)", [1, 2], format_func=lambda x: "1 · Masculino" if x == 1 else "2 · Feminino", horizontal=True)
    idade = b.slider("Idade (anos)", 18, 85, 30)
    renda = a.number_input("Renda anual familiar (US$)", 0.0, 250000.0, 50000.0, step=2500.0)
    escore = b.slider("Escore de alimentação saudável (HEI-2015, 0–100)", 0, 100, 55)
    atv = st.slider("Atividade física semanal (minutos)", 0, 1500, 120, step=10)
    ok = st.form_submit_button("Inferir", type="primary")

if ok:
    df = pd.DataFrame({"Gênero": [genero], "Idade em anos": [idade], "Renda_anual_familiar": [renda],
                       "Escore Saúde": [escore], "Atv_Sem_HR": [atv]})
    r = predict_model(modelo(), data=df)
    p = float(r["prediction_score"].iloc[0]) * 100
    if int(r["prediction_label"].iloc[0]) == 0:
        st.success(f"Sem traços depressivos inferidos (confiança do modelo: {p:.1f}%).")
    else:
        st.error(f"Traços depressivos inferidos (confiança do modelo: {p:.1f}%).")

with st.expander("Resultados do modelo e limitações"):
    st.markdown(
        "Extra Trees (PyCaret): acurácia 94,98%, AUC 0,957, **recall 71,8%**, precisão 92,5%. "
        "Como os casos positivos são minoria, a acurácia sozinha engana: ~28% dos casos reais não são detectados."
    )
