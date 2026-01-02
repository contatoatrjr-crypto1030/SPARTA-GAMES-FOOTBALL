import streamlit as st
import requests
from datetime import datetime

# 1. IDENTIDADE SPARTA
st.set_page_config(page_title="SPARTA GAMES FOOTBALL", layout="wide")
st.title("⚔️ SPARTA GAMES FOOTBALL")

# 2. CONEXÃO VALIDADA (Substitua pela sua chave que deu certo no teste)
SUA_CHAVE_REAL = "SUA_CHAVE_AQUI" 

headers = {
    'x-apisports-key': SUA_CHAVE_REAL
}

# 3. DICIONÁRIO COMPLETO DE LIGAS
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
    "Copa Libertadores": 13
}

# 4. INTERFACE LATERAL
st.sidebar.title("🛡️ MENU SPARTA")
liga_nome = st.sidebar.selectbox("LIGA ELITE:", list(ligas_ids.keys()))
data_alvo = st.sidebar.date_input("DATA DA MINERAÇÃO:", datetime.now())

# 5. MOTOR DE BUSCA PROFISSIONAL
if st.button("🚀 EXECUTAR MINERAÇÃO PROFUNDA"):
    data_str = data_alvo.strftime("%Y-%m-%d")
    id_liga = ligas_ids[liga_nome]
    
    # Temporada 2025 para ligas europeias em Jan/2026
    season = 2025
    
    url = f"https://v3.football.api-sports.io/fixtures?league={id_liga}&season={season}&date={data_str}"
    
    with st.spinner("Minerando dados de elite..."):
        try:
            response = requests.get(url, headers=headers).json()
            
            if response.get('response'):
                jogos = response['response']
                st.success(f"✅ {len(jogos)} JOGOS ENCONTRADOS")
                
                for jogo in jogos:
                    with st.expander(f"🏟️ {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"⏰ **Hora:** {jogo['fixture']['date'][11:16]}")
                            st.write(f"📍 **Estádio:** {jogo['fixture']['venue']['name']}")
                        with col2:
                            st.write(f"📊 **Status:** {jogo['fixture']['status']['long']}")
                            st.info("🎯 DADOS PRO ATIVOS")
            else:
                st.warning(f"Nenhum jogo encontrado para {liga_nome} em {data_str}.")
                
        except Exception as e:
            st.error(f"Erro na mineração: {e}")
