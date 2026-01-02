import streamlit as st
import requests
from datetime import datetime

# 1. SETUP PROFISSIONAL
st.set_page_config(page_title="SPARTA GAMES FOOTBALL", layout="wide")
st.title("⚔️ SPARTA GAMES FOOTBALL")

# 2. AUTENTICAÇÃO DIRETA (Conforme sua documentação)
if "api_key" in st.secrets:
    API_KEY = st.secrets["api_key"]
else:
    st.error("❌ Chave não configurada nos Segredos (Secrets).")
    st.stop()

# AJUSTE DE HOST: Usando o host direto da API-Sports para aceitar sua chave
headers = {
    'x-apisports-key': API_KEY,
    'host': "v3.football.api-sports.io"
}

# 3. INTERFACE
st.sidebar.title("🛡️ TERMINAL SPARTA")
ligas = {
    "Inglaterra: Premier League": 39,
    "Espanha: La Liga": 140,
    "Brasil: Série A": 71,
    "Itália: Serie A": 135
}
liga_nome = st.sidebar.selectbox("ESCOLHA A LIGA:", list(ligas.keys()))
data_alvo = st.sidebar.date_input("DATA DO JOGO:", datetime.now())

# 4. MINERAÇÃO
if st.button("🚀 EXECUTAR MINERAÇÃO PROFUNDA"):
    data_str = data_alvo.strftime("%Y-%m-%d")
    # Para ligas europeias em Jan/2026, a temporada correta no banco de dados é 2025
    season = 2025 if ligas[liga_nome] != 71 else 2025
    
    url = f"https://v3.football.api-sports.io/fixtures?league={ligas[liga_nome]}&season={season}&date={data_str}"
    
    try:
        # Mudamos a forma de chamada para o padrão direto
        response = requests.get(url, headers=headers).json()
        
        if response.get('errors') and len(response['errors']) > 0:
            st.error(f"Erro da API: {response['errors']}")
            st.info("Dica: Verifique se sua chave foi colada corretamente nos Secrets.")
        
        if response.get('response'):
            st.success(f"Sucesso! {len(response['response'])} jogos minerados.")
            for jogo in response['response']:
                with st.expander(f"🏟️ {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}"):
                    st.write(f"⏰ Hora: {jogo['fixture']['date'][11:16]}")
                    st.write(f"📊 Status: {jogo['fixture']['status']['long']}")
                    st.info("🎯 BLOCO C: ANALISAR DESVIOS")
        else:
            st.warning(f"Nenhum jogo encontrado para {data_str} na temporada {season}.")
            
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
