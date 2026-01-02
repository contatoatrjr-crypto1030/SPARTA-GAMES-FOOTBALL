import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="SPARTA GAMES FOOTBALL")
st.title("⚔️ SPARTA GAMES FOOTBALL")

if "api_key" in st.secrets:
    API_KEY = st.secrets["api_key"]
    headers = {'x-rapidapi-key': API_KEY, 'x-rapidapi-host': "v3.football.api-sports.io"}
else:
    st.error("Chave API não configurada nos Segredos (Secrets).")
    st.stop()

st.sidebar.title("MENU")
liga = st.sidebar.selectbox("LIGA:", ["Premier League", "La Liga"])

if st.button("EXECUTAR MINERAÇÃO"):
    st.write("Buscando dados PRO...")
    url = "https://v3.football.api-sports.io/fixtures?league=39&season=2025&date=2026-01-01"
    res = requests.get(url, headers=headers).json()
    st.write(res)
