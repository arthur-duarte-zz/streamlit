import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import plotly.express as px


# -----------------------------
# CARREGAR DADOS
# -----------------------------
@st.cache_data
def carregar_dados():
    query = "SELECT * FROM ed_enem_2024_resultados_amos_per"
    df = df = pd.read_csv('ed_enem_2024_resultados_amos_per.csv')
    return df

df = carregar_dados()

# -----------------------------
# INTERFACE STREAMLIT
# -----------------------------
st.set_page_config(layout="wide")
st.title("Análise da amostra perfeita dos dados do ENEM 2024")

# -----------------------------
# FILTROS
# -----------------------------
st.sidebar.header("Filtros")

ufs = st.sidebar.multiselect(
    "Selecione a UF:",
    options=sorted(df['sg_uf_prova'].dropna().unique()),
    default=None
)

faixa_nota = st.sidebar.slider(
    "Faixa de Nota (Média):",
    0, 1000, (300, 800)
)


# -----------------------------
# APLICAR FILTROS
# -----------------------------
df_filtrado = df.copy()

if ufs:
    df_filtrado = df_filtrado[df_filtrado['sg_uf_prova'].isin(ufs)]

df_filtrado = df_filtrado[
    (df_filtrado['nota_media_5_notas'] >= faixa_nota[0]) &
    (df_filtrado['nota_media_5_notas'] <= faixa_nota[1])
]

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total de Alunos", len(df_filtrado))
col2.metric("Média Geral", round(df_filtrado['nota_media_5_notas'].mean(), 2))
col3.metric("Maior Nota", df_filtrado['nota_media_5_notas'].max(), 2)

# -----------------------------
# GRÁFICOS
# -----------------------------

# 1 Notas por UF
fig_uf_nota = px.bar(
    df_filtrado.groupby('sg_uf_prova')['nota_media_5_notas'].mean().reset_index(),
    x='sg_uf_prova',
    y='nota_media_5_notas',
    title="Média de Nota por UF"
)

# 1 Provas por UF
fig_uf_num = px.bar(
    df_filtrado,
    x='sg_uf_prova',
    title="Número de provars realizadas por UF"
)

# 2 Distribuição de Notas
fig_hist = px.histogram(
    df_filtrado,
    x='nota_media_5_notas',
    nbins=30,
    title="Distribuição das Notas"
)

# 3 Distribuição por Língua Estrangeira
fig_lingua = px.pie(
    df_filtrado,
    names='tp_lingua',
    title="Distribuição de Língua Estrangeira (ENEM)",
    hole=0.6,
    
)

# -----------------------------
# LAYOUT
# -----------------------------
col1, col2 = st.columns(2, gap="large")
col1.plotly_chart(fig_hist, use_container_width=True)
col2.plotly_chart(fig_uf_nota, use_container_width=True)

col5, col6 = st.columns(2, gap ="large")
col5.plotly_chart(fig_lingua, use_container_width=True)
col6.plotly_chart(fig_uf_num, use_container_width=True)