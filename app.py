import streamlit as st
import requests
from datetime import datetime

# 1. SETUP E CHAVE
API_KEY_SPARTA = "0fc8e0ad59e9d1a347cdd2426f7aaa02"
headers = {'x-apisports-key': API_KEY_SPARTA}

st.set_page_config(page_title="SPARTA VEREDITO", layout="wide")
st.title("⚔️ SPARTA GAMES: MINERADOR DE ELITE")

# 2. SELEÇÃO DE LIGA
ligas_ids = {"Premier League": 39, "La Liga": 140, "Serie A": 135, "Brasileirão": 71}
st.sidebar.title("🛡️ FILTROS")
liga_nome = st.sidebar.selectbox("LIGA:", list(ligas_ids.keys()))
data_alvo = st.sidebar.date_input("DATA:", datetime.now())

# 3. MOTOR DE MINERAÇÃO
if st.button("🚀 ENCONTRAR DESVIOS DE VALOR"):
    data_str = data_alvo.strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?league={ligas_ids[liga_nome]}&season=2025&date={data_str}"
    
    with st.spinner("Minerando desvios..."):
        try:
            res = requests.get(url, headers=headers).json()
            if res.get('response'):
                for jogo in res['response']:
                    id_j = jogo['fixture']['id']
                    h, a = jogo['teams']['home']['name'], jogo['teams']['away']['name']
                    
                    # Previsões
                    u_pred = f"https://v3.football.api-sports.io/predictions?fixture={id_j}"
                    r_pred = requests.get(u_pred, headers=headers).json()
                    
                    if r_pred.get('response'):
                        d = r_pred['response'][0]
                        
                        # --- CORREÇÃO DO ERRO DE CONVERSÃO ---
                        try:
                            # Primeiro converte para float, depois para int para remover o '.0'
                            f_h = int(float(d['comparison']['total']['home'].replace('%',''))) if d['comparison']['total']['home'] else 0
                            f_a = int(float(d['comparison']['total']['away'].replace('%',''))) if d['comparison']['total']['away'] else 0
                        except:
                            f_h, f_a = 0, 0
                            
                        desvio = abs(f_h - f_a)
                        conselho = d['predictions']['advice']

                        # --- LÓGICA DE FILTRO SPARTA ---
                        cor = "#FF4B4B" if desvio >= 25 else "#262730"
                        borda = "2px solid #FF4B4B" if desvio >= 25 else "1px solid #555"
                        
                        st.markdown(f"""
                        <div style="border: {borda}; padding: 15px; border-radius: 10px; margin-bottom: 15px; background-color: #0e1117;">
                            <h3 style="color: {cor}; margin:0;">{'🔥 DESVIO ENCONTRADO' if desvio >= 25 else 'Análise Regular'}</h3>
                            <h2 style="margin: 10px 0;">{h} vs {a}</h2>
                            <div style="display: flex; gap: 20px;">
                                <div><b>🏠 Força Casa:</b> {f_h}%</div>
                                <div><b>🚀 Força Fora:</b> {f_a}%</div>
                                <div><b>⚖️ Desvio:</b> {desvio}%</div>
                            </div>
                            <hr style="border: 0.5px solid #444;">
                            <p style="font-size: 18px; color: #00ff00;"><b>🎯 VEREDITO: {conselho}</b></p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("Sem dados para esta liga hoje.")
        except Exception as e:
            st.error(f"Erro na mineração: {e}")
