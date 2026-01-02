import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="SPARTA GAMES FOOTBALL", layout="wide")
st.title("⚔️ SPARTA GAMES FOOTBALL")

# 1. CONEXÃO SEGURA
if "api_key" in st.secrets:
    API_KEY = st.secrets["api_key"]
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': "v3.football.api-sports.io"}
else:
    st.error("Chave API não configurada nos Secrets.")
    st.stop()

# 2. DICIONÁRIO EXPANDIDO (SISTEMA SPARTA TOTAL)
ligas_ids = {
    "Inglaterra: Premier League": 39,
    "Inglaterra: Championship": 40,
    "Espanha: La Liga": 140,
    "Espanha: La Liga 2": 141,
    "Itália: Serie A": 135,
    "Alemanha: Bundesliga": 78,
    "França: Ligue 1": 61,
    "Brasil: Série A": 71,
    "Brasil: Série B": 72,
    "Portugal: Liga Portugal": 94,
    "Holanda: Eredivisie": 88,
    "Bélgica: Pro League": 144,
    "Turquia: Super Lig": 203,
    "Grécia: Super League": 197,
    "Argentina: Liga Profesional": 128,
    "México: Liga MX": 262,
    "Arábia Saudita: Pro League": 307,
    "Champions League": 2,
    "Europa League": 3,
    "Copa Libertadores": 13
}

st.sidebar.title("🛡️ TERMINAL DE ELITE")
# Seletor de Ligas agora com todas as opções acima
liga_nome = st.sidebar.selectbox("ESCOLHA A LIGA ALVO:", list(ligas_ids.keys()))
data_escolhida = st.sidebar.date_input("DATA DO JOGO:", datetime.now())

# 3. MOTOR DE MINERAÇÃO
if st.button("🚀 EXECUTAR MINERAÇÃO PROFUNDA"):
    data_str = data_escolhida.strftime("%Y-%m-%d")
    id_liga = ligas_ids[liga_nome]
    
    st.info(f"Minerando {liga_nome} | Data: {data_str}")
    
    # Busca de Jogos
    url = f"https://v3.football.api-sports.io/fixtures?league={id_liga}&season=2025&date={data_str}"
    
    try:
        response = requests.get(url, headers=headers).json()
        if response.get('response'):
            st.success(f"Encontrados {len(response['response'])} jogos de elite.")
            for jogo in response['response']:
                with st.expander(f"🏟️ {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"⏰ **Hora:** {jogo['fixture']['date'][11:16]}")
                        st.write(f"📍 **Estádio:** {jogo['fixture']['venue']['name']}")
                    with col2:
                        st.write("📊 **Status:** Dados PRO Ativos")
                        st.info("🎯 BLOCO C: FOCO EM DESVIOS")
        else:
            st.warning("Nenhum jogo encontrado para estes filtros.")
    except Exception as e:
        st.error(f"Erro na extração: {e}")
