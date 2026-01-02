import streamlit as st
import requests
from datetime import datetime

# 1. IDENTIDADE VISUAL DARK MODE
st.set_page_config(page_title="SPARTA ELITE", layout="wide")

# CSS para forçar o tema Preto e Branco e melhorar o layout
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stButton>button { width: 100%; background-color: #ffffff; color: #000000; font-weight: bold; border-radius: 0px; }
    .stSelectbox, .stDateInput { background-color: #111111; }
    div[data-testid="stExpander"] { border: 1px solid #333333; border-radius: 0px; background-color: #000000; }
    h1, h2, h3 { color: #ffffff !important; font-family: 'Courier New', Courier, monospace; }
    p, b, span { color: #cccccc !important; }
    .metric-box { border: 1px solid #444444; padding: 10px; text-align: center; }
    .veredito-box { background-color: #ffffff; color: #000000 !important; padding: 15px; font-weight: bold; text-align: center; margin-top: 10px; }
    .veredito-box b { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÃO DE ACESSO
API_KEY_SPARTA = "0fc8e0ad59e9d1a347cdd2426f7aaa02"
headers = {'x-apisports-key': API_KEY_SPARTA}

st.title("⚔️ SPARTA GAMES | DATA MINING")
st.write("---")

# 3. SIDEBAR MINIMALISTA
st.sidebar.title("🛡️ FILTROS")
ligas_ids = {"Premier League": 39, "La Liga": 140, "Serie A": 135, "Brasileirão": 71}
liga_nome = st.sidebar.selectbox("LIGA:", list(ligas_ids.keys()))
data_alvo = st.sidebar.date_input("DATA:", datetime.now())

# 4. MOTOR DE MINERAÇÃO
if st.button("EXECUTAR MINERAÇÃO DE VALOR"):
    data_str = data_alvo.strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?league={ligas_ids[liga_nome]}&season=2025&date={data_str}"
    
    with st.spinner("Acessando API..."):
        try:
            res = requests.get(url, headers=headers).json()
            if res.get('response'):
                for jogo in res['response']:
                    id_j = jogo['fixture']['id']
                    h, a = jogo['teams']['home']['name'], jogo['teams']['away']['name']
                    
                    # Busca Previsões
                    u_pred = f"https://v3.football.api-sports.io/predictions?fixture={id_j}"
                    r_pred = requests.get(u_pred, headers=headers).json()
                    
                    if r_pred.get('response'):
                        d = r_pred['response'][0]
                        try:
                            f_h = int(float(d['comparison']['total']['home'].replace('%',''))) if d['comparison']['total']['home'] else 0
                            f_a = int(float(d['comparison']['total']['away'].replace('%',''))) if d['comparison']['total']['away'] else 0
                            c_h = d['comparison']['corners']['home'] if d['comparison']['corners']['home'] else "0%"
                            c_a = d['comparison']['corners']['away'] if d['comparison']['corners']['away'] else "0%"
                        except: f_h, f_a, c_h, c_a = 0, 0, "0%", "0%"
                            
                        desvio = abs(f_h - f_a)
                        conselho = d['predictions']['advice']

                        # Layout de Cartão Black & White
                        with st.container():
                            st.markdown(f"""
                            <div style="border: 1px solid #444; padding: 20px; margin-bottom: 20px;">
                                <h2 style="text-align: center; margin-bottom: 20px;">{h.upper()} VS {a.upper()}</h2>
                                <div style="display: flex; justify-content: space-around; margin-bottom: 15px;">
                                    <div class="metric-box"><b>FORÇA CASA</b><br><span style="font-size: 20px;">{f_h}%</span></div>
                                    <div class="metric-box"><b>DESVIO</b><br><span style="font-size: 20px; color: #fff !important;">{desvio}%</span></div>
                                    <div class="metric-box"><b>FORÇA FORA</b><br><span style="font-size: 20px;">{f_a}%</span></div>
                                </div>
                                <div style="text-align: center; border-top: 1px solid #333; padding-top: 10px;">
                                    <span>🚩 CANTOS: {c_h} (H) | {c_a} (A)</span>
                                </div>
                                <div class="veredito-box">
                                    VEREDITO: <b>{conselho.upper()}</b>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.warning("Sem dados encontrados.")
        except Exception as e:
            st.error(f"Erro: {e}")

st.sidebar.write("---")
st.sidebar.caption("SISTEMA SPARTA v5.1 | CODED FOR VALUE")
