import streamlit as st
import requests
from datetime import datetime

# =========================================================
# CONFIGURAÇÃO DE ACESSO SPARTA (CHAVE INTEGRADA)
# =========================================================
API_KEY_SPARTA = "0fc8e0ad59e9d1a347cdd2426f7aaa02"
headers = {'x-apisports-key': API_KEY_SPARTA}
# =========================================================

# 1. IDENTIDADE DO TERMINAL
st.set_page_config(page_title="SPARTA GAMES FOOTBALL", layout="wide")
st.title("⚔️ SPARTA GAMES FOOTBALL")
st.markdown("---")

# 2. DICIONÁRIO DE LIGAS ELITE (SISTEMA COMPLETO)
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
    "Arábia Saudita: Pro League": 307,
    "Champions League": 2,
    "Europa League": 3,
    "Copa Libertadores": 13
}

# 3. INTERFACE LATERAL (FILTROS DE MINERAÇÃO)
st.sidebar.title("🛡️ MENU SPARTA")
liga_nome = st.sidebar.selectbox("ESCOLHA A LIGA:", list(ligas_ids.keys()))
data_alvo = st.sidebar.date_input("DATA DA MINERAÇÃO:", datetime.now())

# 4. MOTOR DE MINERAÇÃO DE VALOR
if st.button("🚀 EXECUTAR MINERAÇÃO PROFUNDA"):
    data_str = data_alvo.strftime("%Y-%m-%d")
    id_liga = ligas_ids[liga_nome]
    
    # Temporada 2025 (Necessária para ligas europeias em Jan/2026)
    season = 2025
    
    url_fixtures = f"https://v3.football.api-sports.io/fixtures?league={id_liga}&season={season}&date={data_str}"
    
    with st.spinner("Minerando dados de elite e encontrando desvios..."):
        try:
            res_fix = requests.get(url_fixtures, headers=headers).json()
            
            if res_fix.get('response'):
                jogos = res_fix['response']
                st.success(f"✅ {len(jogos)} JOGOS ENCONTRADOS")
                
                for jogo in jogos:
                    id_jogo = jogo['fixture']['id']
                    time_casa = jogo['teams']['home']['name']
                    time_fora = jogo['teams']['away']['name']
                    
                    # Expander para cada jogo com mineração de Probabilidades
                    with st.expander(f"🏟️ {time_casa} vs {time_fora} - ANALISAR VALOR"):
                        
                        # Chamada para buscar Previsões (Predictions)
                        url_pred = f"https://v3.football.api-sports.io/predictions?fixture={id_jogo}"
                        res_pred = requests.get(url_pred, headers=headers).json()
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write("**📍 Info Geral**")
                            st.write(f"⏰ Hora: {jogo['fixture']['date'][11:16]}")
                            st.write(f"🏟️ Local: {jogo['fixture']['venue']['name']}")
                            st.write(f"📊 Status: {jogo['fixture']['status']['long']}")
                        
                        if res_pred.get('response'):
                            data = res_pred['response'][0]
                            with col2:
                                st.write("**🎲 Probabilidades**")
                                st.write(f"🏆 Favorito: {data['predictions']['winner']['name']}")
                                st.write(f"📈 Força Casa: {data['comparison']['total']['home']}")
                                st.write(f"📉 Força Fora: {data['comparison']['total']['away']}")
                            
                            with col3:
                                st.write("**⚽ Análise de Gols**")
                                st.success(f"Conselho: {data['predictions']['advice']}")
                                st.warning(f"Expectativa: {data['predictions']['goals']['home'] or 'N/A'}")
                        else:
                            st.info("Estatísticas detalhadas não disponíveis para este jogo.")
            else:
                st.warning(f"Nenhum jogo encontrado para {liga_nome} em {data_str}.")
                
        except Exception as e:
            st.error(f"Falha na mineração: {e}")

st.sidebar.write("---")
st.sidebar.caption("SPARTA GAMES FOOTBALL v4.0 - API PRO ATIVA")
