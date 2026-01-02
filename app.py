import streamlit as st
import requests
from datetime import datetime

# 1. SETUP DO TERMINAL
st.set_page_config(page_title="SPARTA GAMES FOOTBALL", layout="wide")
st.title("⚔️ SPARTA GAMES FOOTBALL")

# 2. AUTENTICAÇÃO PURA (Padrão Direto API-Sports)
if "api_key" in st.secrets:
    API_KEY = st.secrets["api_key"]
else:
    st.error("❌ Chave não configurada nos Segredos (Secrets).")
    st.stop()

# CABEÇALHO LIMPO: Conforme sua documentação, sem host adicional para evitar erro 4xSe
headers = {
    'x-apisports-key': API_KEY
}

# 3. DICIONÁRIO COMPLETO DE LIGAS (Sem limitações)
ligas_ids = {
    "Inglaterra: Premier League": 39,
    "Inglaterra: Championship": 40,
    "Espanha: La Liga": 140,
    "Itália: Serie A": 135,
    "Alemanha: Bundesliga": 78,
    "França: Ligue 1": 61,
    "Brasil: Série A": 71,
    "Brasil: Série B": 72,
    "Portugal: Liga Portugal": 94,
    "Holanda: Eredivisie": 88,
    "Arábia Saudita: Pro League": 307,
    "Champions League": 2,
    "Copa Libertadores": 13
}

st.sidebar.title("🛡️ TERMINAL SPARTA")
liga_nome = st.sidebar.selectbox("ESCOLHA A LIGA:", list(ligas_ids.keys()))
data_alvo = st.sidebar.date_input("DATA DO JOGO:", datetime.now())

# 4. MOTOR DE BUSCA (ENDPOINT FIXTURES)
if st.button("🚀 EXECUTAR MINERAÇÃO PROFUNDA"):
    data_str = data_alvo.strftime("%Y-%m-%d")
    id_liga = ligas_ids[liga_nome]
    
    # A temporada na API é definida pelo ano de início (2025 para Europa)
    season = 2025
    
    # URL DIRETA DA API-SPORTS
    url = f"https://v3.football.api-sports.io/fixtures?league={id_liga}&season={season}&date={data_str}"
    
    try:
        # Chamada simplificada para validar o token
        response = requests.get(url, headers=headers).json()
        
        # Se houver erro de token, o sistema reportará exatamente o que a API diz
        if response.get('errors'):
            st.error(f"Erro de Autenticação: {response['errors']}")
        
        elif response.get('response'):
            jogos = response['response']
            if len(jogos) > 0:
                st.success(f"INTEGRAÇÃO CONCLUÍDA: {len(jogos)} jogos encontrados.")
                for jogo in jogos:
                    with st.expander(f"🏟️ {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}"):
                        st.write(f"⏰ Hora: {jogo['fixture']['date'][11:16]}")
                        st.info("🎯 DADOS PRO ATIVOS")
            else:
                st.warning(f"Conectado à API, mas sem jogos para {data_str} na temporada {season}.")
        else:
            st.warning("Resposta da API sem dados. Verifique os créditos do seu plano.")
            
    except Exception as e:
        st.error(f"Erro de Conexão: {e}")
