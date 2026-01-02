import streamlit as st
import requests
from datetime import datetime

# 1. IDENTIDADE VISUAL
st.set_page_config(page_title="SPARTA GAMES FOOTBALL", layout="wide")
st.title("⚔️ SPARTA GAMES FOOTBALL")

# 2. AUTENTICAÇÃO (Conforme Seção Authentication da Doc V3)
if "api_key" in st.secrets:
    API_KEY = st.secrets["api_key"]
else:
    st.error("❌ Chave API não encontrada nos Segredos (Secrets).")
    st.stop()

# Conforme a documentação: x-apisports-key é para acesso direto
headers = {
    'x-apisports-key': API_KEY
}

# 3. FILTROS DE ELITE (Todas as Ligas)
ligas_ids = {
    "Inglaterra: Premier League": 39,
    "Espanha: La Liga": 140,
    "Itália: Serie A": 135,
    "Alemanha: Bundesliga": 78,
    "Brasil: Série A": 71,
    "Brasil: Série B": 72,
    "Portugal: Liga Portugal": 94,
    "Arábia Saudita: Pro League": 307,
    "Champions League": 2
}

st.sidebar.title("🛡️ TERMINAL SPARTA")
liga_nome = st.sidebar.selectbox("LIGA:", list(ligas_ids.keys()))
data_alvo = st.sidebar.date_input("DATA DO JOGO:", datetime.now())

# 4. MINERAÇÃO DIRETA (Endpoint Fixtures)
if st.button("🚀 EXECUTAR MINERAÇÃO PROFUNDA"):
    data_str = data_alvo.strftime("%Y-%m-%d")
    id_liga = ligas_ids[liga_nome]
    
    # IMPORTANTE: Para a API, Jan/2026 ainda é Temporada 2025
    season = 2025
    
    # URL oficial sem o intermediário RapidAPI (Evita Erro 4xSe)
    url = f"https://v3.football.api-sports.io/fixtures?league={id_liga}&season={season}&date={data_str}"
    
    try:
        # Chamada direta ao Host v3.football.api-sports.io
        response = requests.get(url, headers=headers).json()
        
        # Verificação técnica de erro
        if response.get('errors'):
            st.error(f"Erro na Autenticação: {response['errors']}")
            st.info("Dica: Verifique se sua chave está correta no painel da API-Football.")
        
        elif response.get('response'):
            jogos = response['response']
            if len(jogos) > 0:
                st.success(f"DADOS INTEGRADOS: {len(jogos)} jogos encontrados.")
                for jogo in jogos:
                    with st.expander(f"🏟️ {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}"):
                        st.write(f"⏰ Hora: {jogo['fixture']['date'][11:16]}")
                        st.write(f"📊 Status: {jogo['fixture']['status']['long']}")
                        st.info("🎯 DADOS ATIVOS")
            else:
                st.warning(f"Sem jogos em {data_str} (Temporada {season}).")
        else:
            st.error("Resposta inválida da API. Verifique sua assinatura.")
            
    except Exception as e:
        st.error(f"Falha Crítica: {e}")
