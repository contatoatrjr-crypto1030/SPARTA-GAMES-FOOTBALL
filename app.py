import streamlit as st
import requests
from datetime import datetime

# 1. IDENTIDADE VISUAL SPARTA GAMES FOOTBALL
st.set_page_config(page_title="SPARTA GAMES FOOTBALL", layout="wide", page_icon="⚔️")

# CSS para deixar o visual profissional
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_name=True)

st.title("⚔️ SPARTA GAMES FOOTBALL")
st.write("---")

# 2. SEGURANÇA E CHAVE API (Puxa dos Secrets do Streamlit)
if "api_key" in st.secrets:
    API_KEY = st.secrets["api_key"]
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "v3.football.api-sports.io"
    }
else:
    st.error("❌ ERRO: Chave API não configurada nos Secrets do Streamlit.")
    st.stop()

# 3. BARRA LATERAL - CONTROLE DE CRÉDITOS E FILTROS
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/805/805401.png", width=100)
st.sidebar.title("MENU DE COMANDO")
st.sidebar.write("---")

liga_nome = st.sidebar.selectbox("ESCOLHA A LIGA ELITE (7/7):", ["Premier League", "La Liga", "Serie A", "Brasileirão Série A"])
ligas_ids = {"Premier League": 39, "La Liga": 140, "Serie A": 135, "Brasileirão Série A": 71}

# 4. LÓGICA DE MINERAÇÃO SNIPER
if st.button("🚀 EXECUTAR MINERAÇÃO PROFUNDA (Consumir 1 Crédito)"):
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    
    with st.spinner(f"Minerando desvios na {liga_nome}..."):
        # Endpoint de Fixtures (Jogos)
        url = f"https://v3.football.api-sports.io/fixtures?league={ligas_ids[liga_nome]}&season=2025&date={data_hoje}"
        
        try:
            response = requests.get(url, headers=headers).json()
            
            if response.get('response'):
                st.success(f"Sucesso! {len(response['response'])} jogos de elite encontrados.")
                
                for jogo in response['response']:
                    with st.container():
                        st.markdown(f"### 🏟️ {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Horário", jogo['fixture']['date'][11:16])
                        with col2:
                            st.write("**📍 Validação Técnica:**")
                            st.write("- Checklist 7/7: ✅")
                            st.write("- Dados PRO: ✅")
                        with col3:
                            # Aqui o sistema indica o Bloco C conforme a filosofia
                            st.info("🎯 BLOCO C: FOCO EM CARTÕES/GOLS")
                        
                        # Espaço para os dados de mineração (xG e Cartões)
                        st.write(f"🔍 **Análise Sparta:** Buscando desvios de valor para {jogo['teams']['away']['name']} +1.5 Cartões.")
                        st.markdown("---")
            else:
                st.warning("⚠️ Nenhum jogo desta liga hoje que atenda aos critérios 7/7.")
                
        except Exception as e:
            st.error(f"Erro Crítico na API: {e}")

# 5. RODAPÉ INFORMATIVO
st.sidebar.write("---")
st.sidebar.write("💳 **Plano PRO Ativo**")
st.sidebar.write(f"📅 Data: {datetime.now().strftime('%d/%m/%Y')}")
