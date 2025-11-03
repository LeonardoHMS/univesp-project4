import pandas as pd
import plotly.express as px
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Análise de Acidentes 2025", layout="wide")

# Leitura e preparação dos dados
df = pd.read_csv('csv/acidentes2025.csv', encoding='latin1', sep=';')
df['data_inversa'] = pd.to_datetime(df['data_inversa'])
df['hora'] = pd.to_datetime(df['horario'], format='%H:%M:%S').dt.hour
df['idade'] = pd.to_numeric(df['idade'], errors='coerce')
df['feridos_graves'] = pd.to_numeric(df['feridos_graves'], errors='coerce')
df['mortos'] = pd.to_numeric(df['mortos'], errors='coerce')

st.title("🚦 Análise de Acidentes de Trânsito - Brasil 2025")

# Sidebar para filtros
st.sidebar.header("Filtros")
selected_uf = st.sidebar.multiselect("Selecione UF", df['uf'].unique(), default=df['uf'].unique())
selected_tipo_acidente = st.sidebar.multiselect("Tipo de Acidente", df['tipo_acidente'].unique(), default=df['tipo_acidente'].unique())

df_filtered = df[(df['uf'].isin(selected_uf)) & (df['tipo_acidente'].isin(selected_tipo_acidente))]

# --- Acidentes por UF ---
uf_counts = df_filtered['uf'].value_counts().reset_index()
uf_counts.columns = ['UF', 'Quantidade']
st.subheader("Acidentes por Estado (UF)")
fig = px.bar(uf_counts, x='UF', y='Quantidade', text='Quantidade')
st.plotly_chart(fig, use_container_width=True)

# --- Distribuição por horário ---
st.subheader("Distribuição por Hora do Dia")
fig2 = px.histogram(df_filtered, x='hora', nbins=24, title="Acidentes por Hora")
st.plotly_chart(fig2, use_container_width=True)

# --- Principais causas ---
st.subheader("Principais Causas de Acidentes")
causa_counts = df_filtered['causa_acidente'].value_counts().head(10).reset_index()
causa_counts.columns = ['Causa', 'Quantidade']
fig3 = px.bar(causa_counts, x='Causa', y='Quantidade', text='Quantidade')
st.plotly_chart(fig3, use_container_width=True)

# --- Acidentes por dia da semana ---
st.subheader("Acidentes por Dia da Semana")
dia_counts = df_filtered['dia_semana'].value_counts().reindex([
    'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 
    'sexta-feira', 'sábado', 'domingo'
]).reset_index()
dia_counts.columns = ['Dia', 'Quantidade']
fig4 = px.bar(dia_counts, x='Dia', y='Quantidade', text='Quantidade')
st.plotly_chart(fig4, use_container_width=True)

# --- Acidentes por fase do dia ---
st.subheader("Acidentes por Fase do Dia")
fase_counts = df_filtered['fase_dia'].value_counts().reset_index()
fase_counts.columns = ['Fase', 'Quantidade']
fig5 = px.pie(fase_counts, names='Fase', values='Quantidade', title="Distribuição por Fase do Dia")
st.plotly_chart(fig5, use_container_width=True)

# --- Acidentes graves ou mortes ---
st.subheader("Acidentes Graves ou com Mortes")
df_severo = df_filtered[(df_filtered['feridos_graves'] > 0) | (df_filtered['mortos'] > 0)]
fig6 = px.scatter(df_severo, x='hora', y='municipio', size='mortos', color='feridos_graves',
                  hover_data=['tipo_acidente', 'causa_acidente', 'uf'], title="Acidentes Graves e Mortes")
st.plotly_chart(fig6, use_container_width=True)

# --- Tipos de veículos mais envolvidos ---
st.subheader("Tipos de Veículos Envolvidos")
veiculo_counts = df_filtered['tipo_veiculo'].value_counts().reset_index()
veiculo_counts.columns = ['Veículo', 'Quantidade']
fig7 = px.bar(veiculo_counts, x='Veículo', y='Quantidade', text='Quantidade')
st.plotly_chart(fig7, use_container_width=True)

# --- Faixa etária das vítimas ---
st.subheader("Faixa Etária das Vítimas")
fig8 = px.histogram(df_filtered, x='idade', nbins=20, title="Distribuição por Idade")
st.plotly_chart(fig8, use_container_width=True)

# --- Sexo das vítimas ---
st.subheader("Acidentes por Sexo")
sexo_counts = df_filtered['sexo'].value_counts().reset_index()
sexo_counts.columns = ['Sexo', 'Quantidade']
fig9 = px.pie(sexo_counts, names='Sexo', values='Quantidade', title="Distribuição por Sexo")
st.plotly_chart(fig9, use_container_width=True)
