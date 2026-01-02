import streamlit as st
import requests
from datetime import datetime

# 1. IDENTIDADE VISUAL SPARTA GAMES FOOTBALL
st.set_page_config(page_title="SPARTA GAMES FOOTBALL", layout="wide", page_icon="⚔️")

# CSS Corrigido (Removido o parâmetro causador do erro)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚔️ SPARTA GAMES FOOTBALL")
st.write("---")

# 2. SEGURANÇA E CHAVE API
if "api_key" in st.secrets:
    API_KEY = st.secrets["api_key"]
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "v3.football.api-sports.io"
    }
else:
    st.error("❌ ERRO: Chave API não configurada nos Secrets do Streamlit.")
    st.stop()

# 3. BARRA LATERAL
st.sidebar.title("MENU DE COMANDO")
liga_nome = st.sidebar.selectbox("ESCOLHA A LIGA ELITE (7/7):", ["Premier League", "La Liga", "Serie A", "Brasileirão Série A"])
ligas_ids = {"Premier League": 39, "La Liga": 140, "Serie A": 135, "Brasileirão Série A": 71}

# 4. LÓGICA DE MINERAÇÃO
if st.button("🚀 EXECUTAR MINERAÇÃO PROFUNDA"):
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    
    with st.spinner(f"Minerando desvios na {liga_nome}..."):
        url = f"https://v3.football.api-sports.io/fixtures?league={ligas_ids[liga_nome]}&season=2025&date={data_hoje}"
        
        try:
            response = requests.get(url, headers=headers).json()
            
            if response.get('response'):
                st.success(f"Sucesso! {len(response['response'])} jogos encontrados.")
                for jogo in response['response']:
                    with st.container():
                        st.markdown(f"### 🏟️ {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}")
                        c1, c2 = st.columns(2)
                        with c1:
                            st.write(f"⏰ Horário: {jogo['fixture']['date'][11:16]}")
                        with c2:
                            st.info("🎯 BLOCO C: ANALISAR")
                        st.markdown("---")
            else:
                st.warning("⚠️ Nenhum jogo 7/7 encontrado para hoje nesta liga.")
        except Exception as e:
            st.error(f"Erro na conexão: {e}")

st.sidebar.write("---")
st.sidebar.write("🛡️ SPARTA PRO")
