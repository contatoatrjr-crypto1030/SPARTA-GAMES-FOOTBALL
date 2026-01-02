import streamlit as st
import requests
from datetime import datetime

# 1. SETUP E CONEXÃO PRO
API_KEY_SPARTA = "0fc8e0ad59e9d1a347cdd2426f7aaa02"
headers = {'x-apisports-key': API_KEY_SPARTA}

st.set_page_config(page_title="SPARTA VEREDITO", layout="wide")
st.title("⚔️ SPARTA GAMES: MINERADOR DE VEREDITOS")

# 2. SELEÇÃO DE LIGA
ligas_ids = {"Premier League": 39, "La Liga": 140, "Serie A": 135, "Brasileirão": 71, "Champions": 2}
st.sidebar.title("🛡️ FILTROS")
liga_nome = st.sidebar.selectbox("LIGA:", list(ligas_ids.keys()))
data_alvo = st.sidebar.date_input("DATA:", datetime.now())

# 3. MOTOR DE BUSCA E VEREDITO
if st.button("🚀 GERAR VEREDITOS DE VALOR"):
    data_str = data_alvo.strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?league={ligas_ids[liga_nome]}&season=2025&date={data_str}"
    
    with st.spinner("Minerando desvios de valor..."):
        res = requests.get(url, headers=headers).json()
        
        if res.get('response'):
            for jogo in res['response']:
                id_j = jogo['fixture']['id']
                home, away = jogo['teams']['home']['name'], jogo['teams']['away']['name']
                
                # Chamada de Previsões para o Veredito
                u_pred = f"https://v3.football.api-sports.io/predictions?fixture={id_j}"
                r_pred = requests.get(u_pred, headers=headers).json()
                
                if r_pred.get('response'):
                    d = r_pred['response'][0]
                    f_casa = int(d['comparison']['total']['home'].replace('%',''))
                    f_fora = int(d['comparison']['total']['away'].replace('%',''))
                    conselho = d['predictions']['advice']
                    
                    # --- LÓGICA DE VEREDITO SPARTA ---
                    desvio = abs(f_casa - f_fora)
                    cor_alerta = "white"
                    status_valor = "Análise Neutra"
                    
                    if desvio > 40: # Desvio de valor detectado
                        cor_alerta = "#FF4B4B" # Vermelho Sparta
                        status_valor = "🔥 ALERTA DE DESVIO DETECTADO"
                    
                    with st.container():
                        st.markdown(f"""
                        <div style="border: 2px solid {cor_alerta}; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                            <h3 style="color: {cor_alerta};">{status_valor}</h3>
                            <h4>🏟️ {home} vs {away}</h4>
                            <p><b>⚖️ DESVIO DE FORÇA:</b> {desvio}% de diferença</p>
                            <p><b>🎯 VEREDITO SPARTA:</b> {conselho}</p>
                            <p style="font-size: 12px; color: gray;">Status: {jogo['fixture']['status']['long']}</p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.warning("Nenhum jogo minerado para esta data.")
