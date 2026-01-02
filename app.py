import streamlit as st
import requests
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SPARTA GAMES FOOTBALL", layout="wide")

# 2. TÍTULO E ESTILO SIMPLIFICADO (Sem erros)
st.title("⚔️ SPARTA GAMES FOOTBALL")
st.divider()

# 3. VERIFICAÇÃO DA CHAVE API
if "api_key" in st.secrets:
    API_KEY = st.secrets["api_key"]
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "v3.football.api-sports.io"
    }
else:
    st.error("❌ Chave API não configurada nos Secrets do Streamlit.")
    st.stop()

# 4. BARRA LATERAL E FILTROS
st.sidebar.title("MENU SPARTA")
liga_nome = st.sidebar.selectbox("LIGA ELITE (7/7):", ["Premier League", "La Liga", "Serie A", "Brasileirão Série A"])
ligas_ids = {"Premier League": 39, "La Liga": 140, "Serie A": 135, "Brasileirão Série A": 71}

# 5. BOTÃO DE MINERAÇÃO
if st.button("🚀 EXECUTAR MINERAÇÃO PROFUNDA"):
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    st.write(f"🔍 Minerando {liga_nome} para a data: {data_hoje}")
    
    url = f"https://v3.football.api-sports.io/fixtures?league={ligas_ids[liga_nome]}&season=2025&date={data_hoje}"
    
    try:
        response = requests.get(url, headers=headers).json()
        if response.get('response'):
            for jogo in response['response']:
                with st.expander(f"🏟️ {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}"):
                    st.write(f"⏰ Horário: {jogo['fixture']['date'][11:16]}")
                    st.info("🎯 BLOCO C: Analisar Desvios de Valor")
        else:
            st.warning("Nenhum jogo 7/7 encontrado para hoje.")
    except Exception as e:
        st.error(f"Erro na chamada da API: {e}")
