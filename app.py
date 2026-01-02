import streamlit as st
import requests
from datetime import datetime

# 1. SETUP DE ELITE
st.set_page_config(page_title="SPARTA GAMES FOOTBALL", layout="wide")
st.title("⚔️ SPARTA GAMES FOOTBALL")

# 2. AUTENTICAÇÃO DIRETA (Padrão API-Sports PRO)
if "api_key" in st.secrets:
    API_KEY = st.secrets["api_key"]
else:
    st.error("❌ Chave não configurada nos Segredos (Secrets).")
    st.stop()

# Cabeçalho unificado para evitar erro 4xSe
headers = {
    'x-apisports-key': API_KEY
}

# 3. DICIONÁRIO COMPLETO DE LIGAS (Sem limitações)
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
    "Argentina: Liga Profesional": 128,
    "México: Liga MX": 262,
    "Arábia Saudita: Pro League": 307,
    "Champions League": 2,
    "Europa League": 3,
    "Copa Libertadores": 13
}

st.sidebar.title("🛡️ TERMINAL SPARTA")
liga_nome = st.sidebar.selectbox("ESCOLHA A LIGA:", list(ligas_ids.keys()))
data_alvo = st.sidebar.date_input("DATA DO JOGO:", datetime.now())

# 4. MOTOR DE MINERAÇÃO
if st.button("🚀 EXECUTAR MINERAÇÃO PROFUNDA"):
    data_str = data_alvo.strftime("%Y-%m-%d")
    id_liga = ligas_ids[liga_nome]
    
    # Ajuste dinâmico de temporada: Europa (2025), Brasil (2025/2026 conforme a liga)
    season = 2025 
    
    url = f"https://v3.football.api-sports.io/fixtures?league={id_liga}&season={season}&date={data_str}"
    
    try:
        response = requests.get(url, headers=headers).json()
        
        if response.get('errors') and len(response['errors']) > 0:
            st.error(f"Erro de Conexão: {response['errors']}")
        
        elif response.get('response'):
            st.success(f"DADOS INTEGRADOS: {len(response['response'])} jogos encontrados.")
            for jogo in response['response']:
                with st.expander(f"🏟️ {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}"):
                    st.write(f"⏰ Hora: {jogo['fixture']['date'][11:16]}")
                    st.write(f"📊 Status: {jogo['fixture']['status']['long']}")
                    st.info("🎯 DADOS PRO ATIVOS")
        else:
            st.warning(f"Sem jogos para {data_str} na temporada {season}. Verifique a data ou liga.")
            
    except Exception as e:
        st.error(f"Erro Crítico: {e}")
