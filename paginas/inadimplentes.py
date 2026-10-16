import pandas as pd
import plotly.express as px
import streamlit as st
from common import BASE, cabecalho


@st.cache_data
def carregar():
    df = pd.read_csv(BASE / "data" / "credito.csv")
    for c in ["limite_credito", "valor_transacoes_12m"]:
        df[c] = df[c].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["situacao"] = df["default"].map({0: "Adimplente", 1: "Inadimplente"})
    return df


cabecalho("inadimplentes")
df = carregar()

with st.sidebar:
    st.subheader("Filtros (Inadimplentes)")
    sexo = st.multiselect("Sexo", sorted(df["sexo"].dropna().unique()), default=sorted(df["sexo"].dropna().unique()))
    faixa = st.slider("Idade", int(df.idade.min()), int(df.idade.max()), (int(df.idade.min()), int(df.idade.max())))
f = df[df.sexo.isin(sexo) & df.idade.between(*faixa)]

c1, c2, c3 = st.columns(3)
c1.metric("Clientes", f"{len(f):,}".replace(",", "."))
c2.metric("Taxa de inadimplência", f"{f['default'].mean() * 100:.1f}%")
c3.metric("Limite médio (R$)", f"{f['limite_credito'].mean():,.0f}".replace(",", "."))

dim = st.selectbox("Comparar inadimplência por", ["escolaridade", "estado_civil", "salario_anual", "tipo_cartao", "sexo"])
t = f.groupby(dim)["default"].mean().mul(100).round(2).reset_index().sort_values("default", ascending=False)
st.plotly_chart(px.bar(t, x=dim, y="default", labels={"default": "% inadimplentes"}, text="default"), use_container_width=True)

num = st.selectbox("Distribuição de", ["idade", "limite_credito", "valor_transacoes_12m", "qtd_transacoes_12m", "meses_inativo_12m"])
st.plotly_chart(px.box(f, x="situacao", y=num, color="situacao"), use_container_width=True)
with st.expander("Ver dados"):
    st.dataframe(f.head(200))
