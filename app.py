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
    # Ajuste automático de temporada para evitar erro de banco de dados
    season = 2025
    url = f"https://v3.football.api-sports.io/fixtures?league={ligas_ids[liga_nome]}&season={season}&date={data_str}"
    
    with st.spinner("Minerando desvios de valor..."):
        try:
            res = requests.get(url, headers=headers).json()
            
            if res.get('response'):
                for jogo in res['response']:
                    id_j = jogo['fixture']['id']
                    home, away = jogo['teams']['home']['name'], jogo['teams']['away']['name']
                    
                    # Chamada de Previsões
                    u_pred = f"https://v3.football.api-sports.io/predictions?fixture={id_j}"
                    r_pred = requests.get(u_pred, headers=headers).json()
                    
                    if r_pred.get('response'):
                        d = r_pred['response'][0]
                        
                        # TRATAMENTO DE ERRO (VALOR VAZIO)
                        try:
                            val_h = d['comparison']['total']['home']
                            val_a = d['comparison']['total']['away']
                            f_casa = int(val_h.replace('%','')) if val_h else 0
                            f_fora = int(val_fora.replace('%','')) if val_a else 0
                            desvio = abs(f_casa - f_fora)
                        except:
                            desvio = 0
                            
                        conselho = d['predictions']['advice']
                        
                        # --- LÓGICA VISUAL DO VEREDITO ---
                        cor_alerta = "#555" # Cinza padrão
                        status_valor = "Análise Disponível"
                        
                        if desvio >= 30: 
                            cor_alerta = "#FF4B4B" # Vermelho Sparta
                            status_valor = "🔥 ALERTA DE DESVIO DETECTADO"
                        
                        st.markdown(f"""
                        <div style="border: 2px solid {cor_alerta}; padding: 15px; border-radius: 10px; margin-bottom: 10px; background-color: #0e1117;">
                            <h3 style="color: {cor_alerta}; margin-top:0;">{status_valor}</h3>
                            <h4 style="margin-bottom:5px;">🏟️ {home} vs {away}</h4>
                            <p style="margin:2px;"><b>⚖️ DIFERENÇA DE FORÇA:</b> {desvio}%</p>
                            <p style="margin:2px; color: #00ff00;"><b>🎯 VEREDITO: {conselho}</b></p>
                            <p style="font-size: 12px; color: gray; margin-top:10px;">Status: {jogo['fixture']['status']['long']}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("Nenhum jogo encontrado para esta data/liga.")
        except Exception as e:
            st.error(f"Erro na mineração: {e}")
