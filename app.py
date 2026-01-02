import streamlit as st
import requests
from datetime import datetime

# 1. SETUP DE ELITE
st.set_page_config(page_title="SPARTA GAMES FOOTBALL", layout="wide")
st.title("⚔️ SPARTA GAMES FOOTBALL")

# 2. CONFIGURAÇÃO DE CABEÇALHO (Conforme sua documentação)
if "api_key" in st.secrets:
    API_KEY = st.secrets["api_key"]
else:
    st.error("❌ Chave não encontrada nos Segredos (Secrets).")
    st.stop()

# Testaremos os dois padrões de chave para garantir a conexão
headers = {
    'x-apisports-key': API_KEY,
    'x-rapidapi-host': "v3.football.api-sports.io"
}

# 3. INTERFACE DE COMANDO
st.sidebar.title("🛡️ TERMINAL SPARTA")
ligas = {"Premier League": 39, "La Liga": 140, "Serie A": 135, "Brasileirão": 71}
liga_nome = st.sidebar.selectbox("LIGA:", list(ligas.keys()))
data_alvo = st.sidebar.date_input("DATA DO JOGO:", datetime.now())

# 4. MINERAÇÃO DINÂMICA
if st.button("🚀 EXECUTAR MINERAÇÃO PROFUNDA"):
    data_str = data_alvo.strftime("%Y-%m-%d")
    # Ajuste de temporada: Europa (2025), Brasil (2025/2026)
    season = 2025 
    
    url = f"https://v3.football.api-sports.io/fixtures?league={ligas[liga_nome]}&season={season}&date={data_str}"
    
    try:
        response = requests.get(url, headers=headers).json()
        
        # LOG DE DEPURAÇÃO (Aparecerá apenas se houver erro)
        if "errors" in response and response["errors"]:
            st.error(f"Erro da API: {response['errors']}")
        
        if response.get('response'):
            st.success(f"Sucesso! {len(response['response'])} jogos minerados.")
            for jogo in response['response']:
                with st.expander(f"🏟️ {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}"):
                    st.write(f"⏰ Hora: {jogo['fixture']['date'][11:16]}")
                    st.info("🎯 BLOCO C: ANALISAR DESVIOS")
        else:
            st.warning(f"Nenhum jogo em {data_str}. Tente mudar a Data ou a Temporada.")
            
    except Exception as e:
        st.error(f"Erro crítico: {e}")
