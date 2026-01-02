import streamlit as st
import requests

st.title("⚔️ TESTE DE SINAL SPARTA")

# COLOQUE SUA CHAVE DENTRO DAS ASPAS ABAIXO
SUA_CHAVE_REAL = "0fc8e0ad59e9d1a347cdd2426f7aaa02"

headers = {
    'x-apisports-key': SUA_CHAVE_REAL
}

if st.button("🚀 DISPARAR INTEGRAÇÃO"):
    # Testando Premier League (ID 39) na Temporada 2025
    url = "https://v3.football.api-sports.io/fixtures?league=39&season=2025&date=2026-01-01"
    
    try:
        response = requests.get(url, headers=headers).json()
        
        if response.get('response'):
            st.success("✅ SINAL ABERTO! DADOS INTEGRADOS.")
            st.write(f"Jogos encontrados: {len(response['response'])}")
            for jogo in response['response']:
                st.write(f"🏟️ {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}")
        else:
            st.error(f"A API respondeu, mas não encontrou jogos: {response}")
            
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
