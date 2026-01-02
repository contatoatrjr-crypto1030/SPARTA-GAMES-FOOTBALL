import streamlit as st
import requests
from datetime import datetime
import time

# ============================================
# CONFIGURAÇÃO PRINCIPAL
# ============================================
st.set_page_config(page_title="SPARTA FILOSOFIA CENTRAL", layout="wide", initial_sidebar_state="expanded")

API_KEY = "0fc8e0ad59e9d1a347cdd2426f7aaa02"
TIMEZONE = "America/Cuiaba"
HEADERS = {'x-apisports-key': API_KEY}
BASE_URL = "https://v3.football.api-sports.io"

# ============================================
# LIGAS POR TIER
# ============================================
LIGAS_TIER1 = {
    39: 'Premier League',
    140: 'La Liga',
    135: 'Serie A',
    78: 'Bundesliga',
    61: 'Ligue 1',
    2: 'Champions League',
    3: 'Europa League',
    848: 'Conference League',
    71: 'Brasileirão A',
    13: 'Libertadores',
}

LIGAS_TIER2 = {
    88: 'Eredivisie',
    94: 'Primeira Liga',
    144: 'Belgian Pro League',
    40: 'Championship',
    136: 'Serie B Italia',
    72: 'Brasileirão B',
    73: 'Copa do Brasil',
    128: 'Liga Argentina',
    239: 'Super Lig Turquia',
    203: 'Super League Grécia',
}

LIGAS_TIER3 = {
    253: 'MLS',
    262: 'Liga MX',
    179: 'Scottish Premiership',
    113: 'Allsvenskan',
    103: 'Eliteserien',
    119: 'Superligaen',
    218: 'Bundesliga Austria',
    207: 'Super League Suíça',
    235: 'Premier League Rússia',
    333: 'Saudi Pro League',
}

# Casas de apostas para comparar
BOOKMAKERS = {3: "Bet365", 6: "Bwin", 11: "1xBet", 12: "Betway", 16: "Betfair", 27: "Pinnacle"}

def filtrar_por_tier(jogos, tier):
    """Filtra jogos por tier de liga"""
    if tier == 'todos':
        return jogos
    elif tier == 'tier1':
        return [j for j in jogos if j['league']['id'] in LIGAS_TIER1]
    elif tier == 'tier2':
        return [j for j in jogos if j['league']['id'] in LIGAS_TIER1 or j['league']['id'] in LIGAS_TIER2]
    elif tier == 'tier3':
        ids_todos = {**LIGAS_TIER1, **LIGAS_TIER2, **LIGAS_TIER3}
        return [j for j in jogos if j['league']['id'] in ids_todos]
    return jogos

# ============================================
# ESTILO CSS
# ============================================
st.markdown("""
<style>
    .main { background-color: #0a0a0a; }
    [data-testid="stSidebar"] { background-color: #111; border-right: 2px solid #ff0000; }
    .stButton>button { background-color: #ff0000; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #cc0000; }
    h1, h2, h3 { color: #ffffff !important; }
    
    .bloco-a { background: linear-gradient(135deg, #166534, #15803d); padding: 15px; border-radius: 8px; margin: 5px 0; }
    .bloco-b { background: linear-gradient(135deg, #1e40af, #2563eb); padding: 15px; border-radius: 8px; margin: 5px 0; }
    .bloco-c { background: linear-gradient(135deg, #7e22ce, #9333ea); padding: 15px; border-radius: 8px; margin: 5px 0; }
    .bloco-d { background: linear-gradient(135deg, #a16207, #ca8a04); padding: 15px; border-radius: 8px; margin: 5px 0; }
    .bloco-e { background: linear-gradient(135deg, #b91c1c, #dc2626); padding: 15px; border-radius: 8px; margin: 5px 0; }
    
    .value-positivo { background: #166534; color: #4ade80; padding: 8px 15px; border-radius: 4px; font-weight: bold; }
    .value-negativo { background: #7f1d1d; color: #fca5a5; padding: 8px 15px; border-radius: 4px; }
    .joia { background: linear-gradient(135deg, #fbbf24, #f59e0b); color: #000; padding: 10px; border-radius: 8px; font-weight: bold; animation: pulse 2s infinite; }
    
    .lesao-alerta { background: #dc2626; color: white; padding: 5px 10px; border-radius: 4px; font-size: 12px; }
    .odds-melhor { background: #166534; color: #4ade80; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
    
    .veredito-box { background: #ffffff; color: #000000; padding: 15px; font-weight: 900; text-align: center; margin: 10px 0; font-size: 18px; border-radius: 4px; }
    .score-verde { background-color: #166534; padding: 8px 20px; border-radius: 4px; text-align: center; }
    .score-amarelo { background-color: #a16207; padding: 8px 20px; border-radius: 4px; text-align: center; }
    .score-vermelho { background-color: #b91c1c; padding: 8px 20px; border-radius: 4px; text-align: center; }
    
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
</style>
""", unsafe_allow_html=True)

# ============================================
# CONTROLE DE REQUESTS
# ============================================
if 'request_count' not in st.session_state:
    st.session_state['request_count'] = 0

def api_call(endpoint):
    """Faz chamada à API com controle de requests"""
    url = f"{BASE_URL}/{endpoint}"
    try:
        res = requests.get(url, headers=HEADERS)
        st.session_state['request_count'] += 1
        return res.json()
    except Exception as e:
        return {'error': str(e)}

# ============================================
# FUNÇÕES DE BUSCA (TODOS OS ENDPOINTS)
# ============================================
@st.cache_data(ttl=300)
def buscar_jogos(data):
    """Busca todos os jogos de uma data"""
    data_resp = api_call(f"fixtures?date={data}&timezone={TIMEZONE}")
    return data_resp.get('response', [])

@st.cache_data(ttl=300)
def buscar_predictions(fixture_id):
    """Busca predições, H2H, forma"""
    data = api_call(f"predictions?fixture={fixture_id}")
    if data.get('response'):
        return data['response'][0]
    return None

@st.cache_data(ttl=300)
def buscar_odds(fixture_id):
    """Busca odds de todas as casas"""
    data = api_call(f"odds?fixture={fixture_id}")
    return data.get('response', [])

@st.cache_data(ttl=300)
def buscar_injuries(fixture_id):
    """Busca lesões e suspensões"""
    data = api_call(f"injuries?fixture={fixture_id}")
    return data.get('response', [])

@st.cache_data(ttl=600)
def buscar_statistics(fixture_id):
    """Busca estatísticas do jogo (se já iniciou)"""
    data = api_call(f"fixtures/statistics?fixture={fixture_id}")
    return data.get('response', [])

@st.cache_data(ttl=600)
def buscar_lineups(fixture_id):
    """Busca escalações"""
    data = api_call(f"fixtures/lineups?fixture={fixture_id}")
    return data.get('response', [])

@st.cache_data(ttl=3600)
def buscar_standings(league_id, season):
    """Busca classificação da liga"""
    data = api_call(f"standings?league={league_id}&season={season}")
    if data.get('response'):
        return data['response'][0]['league']['standings']
    return []

@st.cache_data(ttl=3600)
def buscar_team_statistics(team_id, league_id, season):
    """Busca estatísticas completas do time"""
    data = api_call(f"teams/statistics?team={team_id}&league={league_id}&season={season}")
    return data.get('response', {})

# ============================================
# FUNÇÕES DE ANÁLISE
# ============================================
def calcular_value(prob_real, odd):
    """Calcula value betting: (prob_real * odd) - 1"""
    if odd <= 0:
        return 0
    value = (prob_real / 100 * odd) - 1
    return round(value * 100, 2)  # retorna em %

def encontrar_melhor_odd(odds_list, mercado="Match Winner"):
    """Encontra a melhor odd entre as casas para cada seleção"""
    melhores = {'home': {'odd': 0, 'casa': ''}, 'draw': {'odd': 0, 'casa': ''}, 'away': {'odd': 0, 'casa': ''}}
    
    for casa in odds_list:
        bookmaker = casa.get('bookmaker', {}).get('name', 'Desconhecida')
        for bet in casa.get('bookmakers', []):
            for market in bet.get('bets', []):
                if market.get('name') == mercado:
                    for value in market.get('values', []):
                        v = value.get('value', '')
                        o = float(value.get('odd', 0))
                        if v == 'Home' and o > melhores['home']['odd']:
                            melhores['home'] = {'odd': o, 'casa': bookmaker}
                        elif v == 'Draw' and o > melhores['draw']['odd']:
                            melhores['draw'] = {'odd': o, 'casa': bookmaker}
                        elif v == 'Away' and o > melhores['away']['odd']:
                            melhores['away'] = {'odd': o, 'casa': bookmaker}
    return melhores

def extrair_odds_mercados(odds_list):
    """Extrai odds de múltiplos mercados"""
    mercados = {
        'match_winner': [],
        'btts': [],
        'over_under_25': [],
        'double_chance': [],
        'corners': []
    }
    
    for casa in odds_list:
        for bookie in casa.get('bookmakers', []):
            bookmaker_name = bookie.get('name', '')
            for market in bookie.get('bets', []):
                nome = market.get('name', '')
                valores = market.get('values', [])
                
                if nome == 'Match Winner':
                    for v in valores:
                        mercados['match_winner'].append({
                            'casa': bookmaker_name,
                            'selecao': v.get('value'),
                            'odd': float(v.get('odd', 0))
                        })
                elif nome == 'Both Teams Score':
                    for v in valores:
                        mercados['btts'].append({
                            'casa': bookmaker_name,
                            'selecao': v.get('value'),
                            'odd': float(v.get('odd', 0))
                        })
                elif 'Over/Under' in nome and '2.5' in nome:
                    for v in valores:
                        mercados['over_under_25'].append({
                            'casa': bookmaker_name,
                            'selecao': v.get('value'),
                            'odd': float(v.get('odd', 0))
                        })
    return mercados

def validar_7_criterios(pred, injuries, odds):
    """Validação completa dos 7 critérios"""
    criterios = []
    score = 0
    
    # 1. Liga conhecida
    criterios.append(("Liga conhecida", True, "✓"))
    score += 1
    
    # 2. Forma recente
    forma_ok = bool(pred.get('teams', {}).get('home', {}).get('league', {}).get('form')) if pred else False
    criterios.append(("Forma recente", forma_ok, pred.get('teams', {}).get('home', {}).get('league', {}).get('form', '-')[:5] if pred else '-'))
    if forma_ok: score += 1
    
    # 3. H2H disponível
    h2h_ok = len(pred.get('h2h', [])) >= 3 if pred else False
    criterios.append(("H2H (3+ jogos)", h2h_ok, f"{len(pred.get('h2h', []))} jogos" if pred else '-'))
    if h2h_ok: score += 1
    
    # 4. Stats de gols
    gols_ok = bool(pred.get('teams', {}).get('home', {}).get('league', {}).get('goals')) if pred else False
    criterios.append(("Stats de gols", gols_ok, "✓" if gols_ok else "✗"))
    if gols_ok: score += 1
    
    # 5. Odds disponíveis
    odds_ok = len(odds) > 0
    criterios.append(("Odds de casas", odds_ok, f"{len(odds)} casas" if odds_ok else "0"))
    if odds_ok: score += 1
    
    # 6. Força comparada
    forca_ok = bool(pred.get('comparison', {}).get('total', {}).get('home')) if pred else False
    criterios.append(("Força comparada", forca_ok, "✓" if forca_ok else "✗"))
    if forca_ok: score += 1
    
    # 7. Lesões checadas
    lesoes_ok = True  # API chamada = check feito
    qtd_lesoes = len(injuries)
    criterios.append(("Lesões checadas", lesoes_ok, f"{qtd_lesoes} ausências" if qtd_lesoes > 0 else "Sem ausências"))
    if lesoes_ok: score += 1
    
    return criterios, score

def identificar_joias(pred, odds_mercados, injuries, blocos):
    """Identifica oportunidades de value betting (joias) com Kelly Criterion"""
    joias = []
    
    if not pred:
        return joias
    
    probs = pred.get('predictions', {}).get('percent', {})
    try:
        prob_home = float(probs.get('home', '0%').replace('%', ''))
        prob_draw = float(probs.get('draw', '0%').replace('%', ''))
        prob_away = float(probs.get('away', '0%').replace('%', ''))
    except:
        return joias
    
    # Ajuste por lesões (reduz probabilidade se time tem lesões importantes)
    home_injuries = len([i for i in injuries if i.get('team', {}).get('name', '') == pred.get('teams', {}).get('home', {}).get('name', '')])
    away_injuries = len([i for i in injuries if i.get('team', {}).get('name', '') == pred.get('teams', {}).get('away', {}).get('name', '')])
    
    # Penalidade de 2% por lesão (máximo 10%)
    prob_home = prob_home * (1 - min(0.10, home_injuries * 0.02))
    prob_away = prob_away * (1 - min(0.10, away_injuries * 0.02))
    
    # Buscar melhores odds para Match Winner
    for item in odds_mercados.get('match_winner', []):
        if item['selecao'] == 'Home':
            value = calcular_value(prob_home, item['odd'])
            bloco = determinar_bloco(item['odd'], value, blocos)
            if bloco:
                kelly_pct = calcular_kelly(prob_home, item['odd']) * 100
                stake = calcular_stake_kelly(prob_home, item['odd'], blocos[bloco]['valor'])
                joias.append({
                    'tipo': '🏠 VITÓRIA CASA',
                    'mercado': 'Match Winner',
                    'odd': item['odd'],
                    'casa': item['casa'],
                    'prob_real': round(prob_home, 1),
                    'value': value,
                    'bloco': bloco,
                    'kelly_pct': round(kelly_pct, 2),
                    'stake_kelly': stake,
                    'stake_max': blocos[bloco]['valor']
                })
        elif item['selecao'] == 'Draw':
            value = calcular_value(prob_draw, item['odd'])
            bloco = determinar_bloco(item['odd'], value, blocos)
            if bloco:
                kelly_pct = calcular_kelly(prob_draw, item['odd']) * 100
                stake = calcular_stake_kelly(prob_draw, item['odd'], blocos[bloco]['valor'])
                joias.append({
                    'tipo': '🤝 EMPATE',
                    'mercado': 'Match Winner',
                    'odd': item['odd'],
                    'casa': item['casa'],
                    'prob_real': round(prob_draw, 1),
                    'value': value,
                    'bloco': bloco,
                    'kelly_pct': round(kelly_pct, 2),
                    'stake_kelly': stake,
                    'stake_max': blocos[bloco]['valor']
                })
        elif item['selecao'] == 'Away':
            value = calcular_value(prob_away, item['odd'])
            bloco = determinar_bloco(item['odd'], value, blocos)
            if bloco:
                kelly_pct = calcular_kelly(prob_away, item['odd']) * 100
                stake = calcular_stake_kelly(prob_away, item['odd'], blocos[bloco]['valor'])
                joias.append({
                    'tipo': '✈️ VITÓRIA FORA',
                    'mercado': 'Match Winner',
                    'odd': item['odd'],
                    'casa': item['casa'],
                    'prob_real': round(prob_away, 1),
                    'value': value,
                    'bloco': bloco,
                    'kelly_pct': round(kelly_pct, 2),
                    'stake_kelly': stake,
                    'stake_max': blocos[bloco]['valor']
                })
    
    # Análise BTTS
    teams = pred.get('teams', {})
    home_goals = teams.get('home', {}).get('league', {}).get('goals', {})
    away_goals = teams.get('away', {}).get('league', {}).get('goals', {})
    
    if home_goals and away_goals:
        try:
            home_for = float(home_goals.get('for', {}).get('average', {}).get('total', 0))
            home_against = float(home_goals.get('against', {}).get('average', {}).get('total', 0))
            away_for = float(away_goals.get('for', {}).get('average', {}).get('total', 0))
            away_against = float(away_goals.get('against', {}).get('average', {}).get('total', 0))
            
            # Probabilidade estimada de BTTS (fórmula melhorada)
            prob_home_marca = min(95, (home_for + away_against) / 2 * 35)
            prob_away_marca = min(95, (away_for + home_against) / 2 * 35)
            prob_btts = (prob_home_marca / 100) * (prob_away_marca / 100) * 100
            
            for item in odds_mercados.get('btts', []):
                if item['selecao'] == 'Yes':
                    value = calcular_value(prob_btts, item['odd'])
                    bloco = determinar_bloco(item['odd'], value, blocos)
                    if bloco:
                        kelly_pct = calcular_kelly(prob_btts, item['odd']) * 100
                        stake = calcular_stake_kelly(prob_btts, item['odd'], blocos[bloco]['valor'])
                        joias.append({
                            'tipo': '⚽ BTTS SIM',
                            'mercado': 'Both Teams Score',
                            'odd': item['odd'],
                            'casa': item['casa'],
                            'prob_real': round(prob_btts, 1),
                            'value': value,
                            'bloco': bloco,
                            'kelly_pct': round(kelly_pct, 2),
                            'stake_kelly': stake,
                            'stake_max': blocos[bloco]['valor']
                        })
            
            # Over/Under 2.5
            media_gols = home_for + away_for
            prob_over = min(85, media_gols * 22)
            
            for item in odds_mercados.get('over_under_25', []):
                if 'Over' in item['selecao']:
                    value = calcular_value(prob_over, item['odd'])
                    bloco = determinar_bloco(item['odd'], value, blocos)
                    if bloco:
                        kelly_pct = calcular_kelly(prob_over, item['odd']) * 100
                        stake = calcular_stake_kelly(prob_over, item['odd'], blocos[bloco]['valor'])
                        joias.append({
                            'tipo': '📈 OVER 2.5',
                            'mercado': 'Over/Under 2.5',
                            'odd': item['odd'],
                            'casa': item['casa'],
                            'prob_real': round(prob_over, 1),
                            'value': value,
                            'bloco': bloco,
                            'kelly_pct': round(kelly_pct, 2),
                            'stake_kelly': stake,
                            'stake_max': blocos[bloco]['valor']
                        })
                elif 'Under' in item['selecao']:
                    prob_under = 100 - prob_over
                    value = calcular_value(prob_under, item['odd'])
                    bloco = determinar_bloco(item['odd'], value, blocos)
                    if bloco:
                        kelly_pct = calcular_kelly(prob_under, item['odd']) * 100
                        stake = calcular_stake_kelly(prob_under, item['odd'], blocos[bloco]['valor'])
                        joias.append({
                            'tipo': '📉 UNDER 2.5',
                            'mercado': 'Over/Under 2.5',
                            'odd': item['odd'],
                            'casa': item['casa'],
                            'prob_real': round(prob_under, 1),
                            'value': value,
                            'bloco': bloco,
                            'kelly_pct': round(kelly_pct, 2),
                            'stake_kelly': stake,
                            'stake_max': blocos[bloco]['valor']
                        })
        except:
            pass
    
    # Ordenar por value
    joias.sort(key=lambda x: x['value'], reverse=True)
    return joias

def calcular_blocos(banca):
    """Distribuição dos 5 blocos - Nova estrutura otimizada"""
    return {
        'A': {'nome': 'Cofre', 'pct': 35, 'valor': banca * 0.35, 'odds_min': 1.20, 'odds_max': 1.80, 'value_min': 3, 'cor': 'bloco-a', 'desc': 'Preservação'},
        'B': {'nome': 'Base', 'pct': 30, 'valor': banca * 0.30, 'odds_min': 1.80, 'odds_max': 2.50, 'value_min': 5, 'cor': 'bloco-b', 'desc': 'Crescimento'},
        'C': {'nome': 'Valor', 'pct': 25, 'valor': banca * 0.25, 'odds_min': 2.50, 'odds_max': 5.00, 'value_min': 8, 'cor': 'bloco-c', 'desc': 'Value betting'},
        'D': {'nome': 'Risco', 'pct': 8, 'valor': banca * 0.08, 'odds_min': 5.00, 'odds_max': 15.00, 'value_min': 15, 'cor': 'bloco-d', 'desc': 'Zebras calculadas'},
        'E': {'nome': 'Loteria', 'pct': 2, 'valor': banca * 0.02, 'odds_min': 15.00, 'odds_max': 999.00, 'value_min': 25, 'cor': 'bloco-e', 'desc': 'Multiplicadores'},
    }

def calcular_kelly(prob_real, odd, fracao=0.25):
    """
    Calcula stake pelo Kelly Criterion fracionário
    prob_real: probabilidade real estimada (ex: 55 para 55%)
    odd: odd decimal
    fracao: fração do Kelly (0.25 = 1/4 Kelly, mais conservador)
    """
    if odd <= 1 or prob_real <= 0:
        return 0
    
    p = prob_real / 100  # converter para decimal
    q = 1 - p
    b = odd - 1  # lucro líquido por unidade
    
    # Fórmula Kelly: (bp - q) / b
    kelly = (b * p - q) / b
    
    # Se Kelly negativo, não apostar
    if kelly <= 0:
        return 0
    
    # Aplicar fração (Kelly fracionário)
    kelly_fracionario = kelly * fracao
    
    # Limitar a 25% máximo por aposta (segurança extra)
    return min(kelly_fracionario, 0.25)

def determinar_bloco(odd, value, blocos):
    """Determina qual bloco a aposta pertence baseado em odd e value"""
    for letra, info in blocos.items():
        if info['odds_min'] <= odd < info['odds_max'] and value >= info['value_min']:
            return letra
    return None

def calcular_stake_kelly(prob_real, odd, bloco_valor, fracao=0.25):
    """Calcula o stake em R$ usando Kelly dentro do bloco"""
    kelly_pct = calcular_kelly(prob_real, odd, fracao)
    stake = kelly_pct * bloco_valor
    
    # Stake mínimo R$ 1 se Kelly > 0
    if stake > 0 and stake < 1:
        stake = 1
    
    return round(stake, 2)

# ============================================
# INTERFACE PRINCIPAL
# ============================================
st.title("⚔️ SPARTA + FILOSOFIA CENTRAL")
st.caption(f"Sistema v7.2 + Kelly + Gestão | Timezone: Cuiabá | Requests: {st.session_state['request_count']}/7.500")
st.markdown("---")

# ============================================
# GESTÃO DE BANCA E HISTÓRICO
# ============================================
if 'historico_apostas' not in st.session_state:
    st.session_state['historico_apostas'] = []

if 'caixa_total' not in st.session_state:
    st.session_state['caixa_total'] = 1100.0

if 'reserva' not in st.session_state:
    st.session_state['reserva'] = 600.0

if 'banca_ativa' not in st.session_state:
    st.session_state['banca_ativa'] = 500.0

def adicionar_aposta(jogo, mercado, selecao, odd, stake, casa):
    """Adiciona aposta ao histórico"""
    aposta = {
        'id': len(st.session_state['historico_apostas']) + 1,
        'data': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'jogo': jogo,
        'mercado': mercado,
        'selecao': selecao,
        'odd': odd,
        'stake': stake,
        'casa': casa,
        'status': 'pendente',
        'retorno': 0,
        'lucro': 0
    }
    st.session_state['historico_apostas'].append(aposta)
    st.session_state['banca_ativa'] -= stake
    return aposta['id']

def atualizar_resultado(aposta_id, status, retorno_real=0):
    """Atualiza resultado da aposta"""
    for aposta in st.session_state['historico_apostas']:
        if aposta['id'] == aposta_id:
            aposta['status'] = status
            if status == 'ganhou':
                aposta['retorno'] = aposta['stake'] * aposta['odd']
                aposta['lucro'] = aposta['retorno'] - aposta['stake']
                st.session_state['banca_ativa'] += aposta['retorno']
            elif status == 'perdeu':
                aposta['retorno'] = 0
                aposta['lucro'] = -aposta['stake']
            elif status == 'cashout':
                aposta['retorno'] = retorno_real
                aposta['lucro'] = retorno_real - aposta['stake']
                st.session_state['banca_ativa'] += retorno_real
            elif status == 'void':
                aposta['retorno'] = aposta['stake']
                aposta['lucro'] = 0
                st.session_state['banca_ativa'] += aposta['stake']
            break

def calcular_estatisticas():
    """Calcula estatísticas do histórico"""
    historico = st.session_state['historico_apostas']
    if not historico:
        return {'total': 0, 'ganhas': 0, 'perdidas': 0, 'pendentes': 0, 'roi': 0, 'lucro_total': 0, 'stake_total': 0}
    
    finalizadas = [a for a in historico if a['status'] in ['ganhou', 'perdeu', 'cashout']]
    ganhas = len([a for a in historico if a['status'] == 'ganhou'])
    perdidas = len([a for a in historico if a['status'] == 'perdeu'])
    pendentes = len([a for a in historico if a['status'] == 'pendente'])
    cashouts = len([a for a in historico if a['status'] == 'cashout'])
    
    lucro_total = sum([a['lucro'] for a in finalizadas])
    stake_total = sum([a['stake'] for a in finalizadas])
    roi = (lucro_total / stake_total * 100) if stake_total > 0 else 0
    
    return {
        'total': len(historico),
        'ganhas': ganhas,
        'perdidas': perdidas,
        'cashouts': cashouts,
        'pendentes': pendentes,
        'roi': round(roi, 2),
        'lucro_total': round(lucro_total, 2),
        'stake_total': round(stake_total, 2),
        'taxa_acerto': round(ganhas / len(finalizadas) * 100, 1) if finalizadas else 0
    }

# ============================================
# SIDEBAR - GESTÃO DE BANCA
# ============================================
st.sidebar.markdown("## 💰 GESTÃO DE CAIXA")

col_s1, col_s2 = st.sidebar.columns(2)
with col_s1:
    novo_caixa = st.number_input("Caixa Total:", value=st.session_state['caixa_total'], min_value=0.0, step=50.0, key='input_caixa')
with col_s2:
    nova_reserva = st.number_input("Reserva:", value=st.session_state['reserva'], min_value=0.0, step=50.0, key='input_reserva')

# Atualizar valores
if novo_caixa != st.session_state['caixa_total']:
    st.session_state['caixa_total'] = novo_caixa
if nova_reserva != st.session_state['reserva']:
    st.session_state['reserva'] = nova_reserva
    st.session_state['banca_ativa'] = st.session_state['caixa_total'] - nova_reserva

banca = st.session_state['banca_ativa']

st.sidebar.markdown(f"""
<div style="background: #1a1a1a; border: 1px solid #333; padding: 10px; border-radius: 8px; margin: 10px 0;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
        <span style="color: #888;">Caixa Total:</span>
        <span style="color: #fff; font-weight: bold;">R$ {st.session_state['caixa_total']:.2f}</span>
    </div>
    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
        <span style="color: #888;">Reserva:</span>
        <span style="color: #fbbf24; font-weight: bold;">R$ {st.session_state['reserva']:.2f}</span>
    </div>
    <div style="display: flex; justify-content: space-between; border-top: 1px solid #333; padding-top: 5px;">
        <span style="color: #888;">Banca Ativa:</span>
        <span style="color: #4ade80; font-weight: bold; font-size: 18px;">R$ {banca:.2f}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Estatísticas rápidas
stats = calcular_estatisticas()
if stats['total'] > 0:
    cor_roi = '#4ade80' if stats['roi'] >= 0 else '#f87171'
    cor_lucro = '#4ade80' if stats['lucro_total'] >= 0 else '#f87171'
    st.sidebar.markdown(f"""
    <div style="background: #111; border: 1px solid #333; padding: 10px; border-radius: 8px; margin: 10px 0;">
        <div style="color: #888; font-size: 12px; margin-bottom: 5px;">📊 PERFORMANCE</div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: #888;">ROI:</span>
            <span style="color: {cor_roi}; font-weight: bold;">{stats['roi']}%</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: #888;">Lucro:</span>
            <span style="color: {cor_lucro}; font-weight: bold;">R$ {stats['lucro_total']}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: #888;">Taxa:</span>
            <span style="color: #fff;">{stats['taxa_acerto']}% ({stats['ganhas']}/{stats['ganhas']+stats['perdidas']})</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("### 📊 BLOCOS")
blocos = calcular_blocos(banca)
for letra, info in blocos.items():
    st.sidebar.markdown(f"""
    <div class="{info['cor']}">
        <strong>BLOCO {letra}</strong> - {info['nome']}<br>
        <span style="font-size: 18px;">R$ {info['valor']:.2f}</span><br>
        <small>{info['pct']}% | Odds: {info['odds_min']}-{info['odds_max']} | Value ≥{info['value_min']}%</small>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Requests:** {st.session_state['request_count']}/7.500")
st.sidebar.progress(st.session_state['request_count'] / 7500)

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ KELLY CRITERION")
st.sidebar.markdown("""
<small>
**Fórmula:** (prob × odd - 1) / (odd - 1) × 25%<br><br>
**Usando Kelly 1/4 (conservador)**<br>
- Maximiza crescimento de longo prazo<br>
- Reduz volatilidade<br>
- Stake proporcional ao value<br><br>
**Regras:**<br>
- Kelly ≤ 0 = não apostar<br>
- Kelly máx = 25% do bloco
</small>
""", unsafe_allow_html=True)

# ============================================
# TABS PRINCIPAIS
# ============================================
tab1, tab2, tab3, tab4 = st.tabs(["📅 JOGOS", "💎 JOIAS", "📊 ANÁLISE", "📋 HISTÓRICO"])

# ============================================
# TAB 1: JOGOS DO DIA
# ============================================
with tab1:
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        data_sel = st.date_input("Data:", datetime.now())
    with col2:
        tier_sel = st.selectbox("Tier:", ['tier1', 'tier2', 'tier3', 'todos'], format_func=lambda x: {
            'tier1': '🏆 Tier 1 (Top 10)',
            'tier2': '🥈 Tier 1+2',
            'tier3': '🥉 Tier 1+2+3',
            'todos': '🌍 Todas Ligas'
        }[x])
    with col3:
        st.write("")
        buscar = st.button("🔍 BUSCAR", use_container_width=True)
    
    if buscar:
        with st.spinner("Buscando jogos..."):
            jogos = buscar_jogos(data_sel.strftime('%Y-%m-%d'))
            st.session_state['jogos'] = jogos
            st.session_state['tier_selecionado'] = tier_sel
    
    if 'jogos' in st.session_state and st.session_state['jogos']:
        jogos = st.session_state['jogos']
        tier_atual = st.session_state.get('tier_selecionado', 'tier1')
        
        # Aplicar filtro de tier
        jogos_filtrados = filtrar_por_tier(jogos, tier_atual)
        
        # Extrair ligas dos jogos filtrados
        ligas = {}
        for j in jogos_filtrados:
            lid = j['league']['id']
            if lid not in ligas:
                ligas[lid] = {'nome': j['league']['name'], 'pais': j['league']['country'], 'jogos': []}
            ligas[lid]['jogos'].append(j)
        
        st.success(f"✅ {len(jogos_filtrados)} jogos em {len(ligas)} ligas ({tier_atual.upper()})")
        
        # Filtro adicional por liga específica
        opcoes = ["🎯 TODAS DO TIER"] + [f"{v['pais']} - {v['nome']} ({len(v['jogos'])})" for k, v in sorted(ligas.items(), key=lambda x: x[1]['pais'])]
        liga_sel = st.selectbox("Filtrar liga:", opcoes)
        
        if liga_sel != "🎯 TODAS DO TIER":
            nome_liga = liga_sel.split(" - ")[1].split(" (")[0]
            jogos_filtrados = [j for j in jogos_filtrados if j['league']['name'] == nome_liga]
        
        # Lista de jogos
        for jogo in sorted(jogos_filtrados, key=lambda x: x['fixture']['date']):
            fixture = jogo['fixture']
            teams = jogo['teams']
            goals = jogo['goals']
            league = jogo['league']
            
            horario = datetime.fromisoformat(fixture['date'].replace('Z', '+00:00')).strftime('%H:%M')
            status = fixture['status']['short']
            
            # Badge de tier
            tier_badge = ""
            if league['id'] in LIGAS_TIER1:
                tier_badge = "🏆"
            elif league['id'] in LIGAS_TIER2:
                tier_badge = "🥈"
            elif league['id'] in LIGAS_TIER3:
                tier_badge = "🥉"
            
            if status == 'NS':
                status_txt = "⏳"
            elif status in ['1H', '2H', 'HT']:
                status_txt = f"🔴 {fixture['status']['elapsed']}'"
            else:
                status_txt = "✅"
            
            placar = f" | {goals['home']}-{goals['away']}" if goals['home'] is not None else ""
            
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"{tier_badge} **{horario}** {status_txt} | {teams['home']['name']} vs {teams['away']['name']}{placar}")
                st.caption(f"{league['country']} • {league['name']}")
            with col2:
                if st.button("📊", key=f"sel_{fixture['id']}"):
                    st.session_state['jogo_sel'] = jogo
                    st.session_state['fixture_id'] = fixture['id']
                    st.session_state['league_id'] = league['id']
                    st.session_state['season'] = league.get('season', 2025)

# ============================================
# TAB 2: JOIAS (VALUE BETTING)
# ============================================
with tab2:
    if 'jogo_sel' not in st.session_state:
        st.info("👆 Selecione um jogo na aba JOGOS")
    else:
        jogo = st.session_state['jogo_sel']
        fixture_id = st.session_state['fixture_id']
        
        st.markdown(f"### 💎 JOIAS: {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}")
        
        with st.spinner("Minerando dados completos..."):
            pred = buscar_predictions(fixture_id)
            odds = buscar_odds(fixture_id)
            injuries = buscar_injuries(fixture_id)
        
        if odds:
            odds_mercados = extrair_odds_mercados(odds)
            joias = identificar_joias(pred, odds_mercados, injuries, blocos)
            
            if joias:
                st.success(f"🎯 {len(joias)} JOIAS ENCONTRADAS!")
                
                # Resumo por bloco
                joias_por_bloco = {}
                for j in joias:
                    b = j['bloco']
                    if b not in joias_por_bloco:
                        joias_por_bloco[b] = []
                    joias_por_bloco[b].append(j)
                
                st.markdown("#### 📊 Resumo por Bloco:")
                cols = st.columns(5)
                for i, letra in enumerate(['A', 'B', 'C', 'D', 'E']):
                    with cols[i]:
                        qtd = len(joias_por_bloco.get(letra, []))
                        st.metric(f"Bloco {letra}", f"{qtd} joias")
                
                st.markdown("---")
                
                for joia in joias:
                    retorno_potencial = joia['stake_kelly'] * joia['odd']
                    lucro_potencial = retorno_potencial - joia['stake_kelly']
                    
                    st.markdown(f"""
                    <div class="joia">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong style="font-size: 18px;">{joia['tipo']}</strong><br>
                                <small>Mercado: {joia['mercado']} | Casa: {joia['casa']}</small>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 24px;">ODD {joia['odd']}</div>
                                <div style="background: #166534; color: #4ade80; padding: 5px 10px; border-radius: 4px;">
                                    VALUE: +{joia['value']}%
                                </div>
                            </div>
                        </div>
                        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(0,0,0,0.2); display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                            <div>
                                <small style="color: #666;">PROBABILIDADE</small><br>
                                <strong>{joia['prob_real']}%</strong>
                            </div>
                            <div>
                                <small style="color: #666;">BLOCO</small><br>
                                <strong>{joia['bloco']} - {blocos[joia['bloco']]['nome']}</strong>
                            </div>
                            <div>
                                <small style="color: #666;">KELLY</small><br>
                                <strong>{joia['kelly_pct']}%</strong>
                            </div>
                            <div style="background: #166534; padding: 8px 15px; border-radius: 4px;">
                                <small style="color: #9fdf9f;">STAKE KELLY</small><br>
                                <strong style="font-size: 18px; color: #4ade80;">R$ {joia['stake_kelly']:.2f}</strong>
                            </div>
                            <div>
                                <small style="color: #666;">RETORNO</small><br>
                                <strong style="color: #4ade80;">R$ {retorno_potencial:.2f}</strong>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.write("")
                
                # Totais
                total_stake = sum([j['stake_kelly'] for j in joias])
                total_retorno = sum([j['stake_kelly'] * j['odd'] for j in joias])
                st.markdown(f"""
                <div style="background: #1a1a1a; border: 2px solid #ff0000; padding: 15px; border-radius: 8px; margin-top: 20px;">
                    <h3 style="margin: 0; color: #fff;">📋 RESUMO DO JOGO</h3>
                    <div style="display: flex; justify-content: space-around; margin-top: 15px;">
                        <div style="text-align: center;">
                            <div style="color: #888;">Total Joias</div>
                            <div style="font-size: 24px; font-weight: bold;">{len(joias)}</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="color: #888;">Investimento Total</div>
                            <div style="font-size: 24px; font-weight: bold;">R$ {total_stake:.2f}</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="color: #888;">Retorno Potencial</div>
                            <div style="font-size: 24px; font-weight: bold; color: #4ade80;">R$ {total_retorno:.2f}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Registrar apostas
                st.markdown("---")
                st.markdown("### 📝 REGISTRAR APOSTA")
                
                joia_opcoes = [f"{j['tipo']} @ {j['odd']} ({j['casa']}) - R$ {j['stake_kelly']:.2f}" for j in joias]
                joia_sel = st.selectbox("Selecione a joia:", joia_opcoes, key="sel_joia_registrar")
                
                if st.button("✅ REGISTRAR ESTA APOSTA", key="btn_registrar"):
                    idx = joia_opcoes.index(joia_sel)
                    j = joias[idx]
                    nome_jogo = f"{jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}"
                    aposta_id = adicionar_aposta(
                        jogo=nome_jogo,
                        mercado=j['mercado'],
                        selecao=j['tipo'],
                        odd=j['odd'],
                        stake=j['stake_kelly'],
                        casa=j['casa']
                    )
                    st.success(f"✅ Aposta #{aposta_id} registrada! Banca atualizada: R$ {st.session_state['banca_ativa']:.2f}")
                    st.rerun()
            else:
                st.warning("⚠️ Nenhuma joia encontrada neste jogo. Odds não atendem aos critérios de value mínimo por bloco.")
        else:
            st.error("❌ Odds não disponíveis para este jogo")

# ============================================
# TAB 3: ANÁLISE COMPLETA
# ============================================
with tab3:
    if 'jogo_sel' not in st.session_state:
        st.info("👆 Selecione um jogo na aba JOGOS")
    else:
        jogo = st.session_state['jogo_sel']
        fixture_id = st.session_state['fixture_id']
        
        st.markdown(f"### {jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}")
        st.caption(f"{jogo['league']['country']} • {jogo['league']['name']}")
        
        with st.spinner("Carregando análise completa..."):
            pred = buscar_predictions(fixture_id)
            odds = buscar_odds(fixture_id)
            injuries = buscar_injuries(fixture_id)
        
        # VALIDAÇÃO 7 CRITÉRIOS
        st.markdown("### ✅ VALIDAÇÃO 7 CRITÉRIOS")
        criterios, score = validar_7_criterios(pred, injuries, odds)
        
        if score >= 5:
            cor = "score-verde"
            rec = "✅ APROVADO"
        elif score >= 3:
            cor = "score-amarelo"
            rec = "⚠️ CAUTELA"
        else:
            cor = "score-vermelho"
            rec = "❌ REJEITAR"
        
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f'<div class="{cor}"><h2>{score}/7</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f"**{rec}**")
        
        cols = st.columns(7)
        for i, (nome, ok, detalhe) in enumerate(criterios):
            with cols[i]:
                cor = "#4ade80" if ok else "#f87171"
                st.markdown(f'<div style="color:{cor}; text-align:center;">{"✓" if ok else "✗"}<br><small>{nome}</small><br><small style="color:#888;">{detalhe}</small></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # LESÕES
        if injuries:
            st.markdown("### 🏥 LESÕES E SUSPENSÕES")
            for inj in injuries:
                player = inj.get('player', {}).get('name', 'Desconhecido')
                team = inj.get('team', {}).get('name', '')
                reason = inj.get('player', {}).get('reason', 'Indisponível')
                st.markdown(f'<span class="lesao-alerta">⚠️ {team}: {player} - {reason}</span>', unsafe_allow_html=True)
            st.write("")
        
        # VEREDITO
        if pred and pred.get('predictions', {}).get('advice'):
            st.markdown(f'<div class="veredito-box">VEREDITO API: {pred["predictions"]["advice"]}</div>', unsafe_allow_html=True)
        
        # PROBABILIDADES
        if pred:
            st.markdown("### 📈 PROBABILIDADES")
            col1, col2, col3 = st.columns(3)
            probs = pred.get('predictions', {}).get('percent', {})
            with col1:
                st.metric("🏠 CASA", probs.get('home', '-'))
            with col2:
                st.metric("🤝 EMPATE", probs.get('draw', '-'))
            with col3:
                st.metric("✈️ FORA", probs.get('away', '-'))
        
        # COMPARADOR DE ODDS
        if odds:
            st.markdown("### 💹 COMPARADOR DE ODDS")
            odds_mercados = extrair_odds_mercados(odds)
            
            # Match Winner
            mw = odds_mercados.get('match_winner', [])
            if mw:
                home_odds = [x for x in mw if x['selecao'] == 'Home']
                draw_odds = [x for x in mw if x['selecao'] == 'Draw']
                away_odds = [x for x in mw if x['selecao'] == 'Away']
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("**CASA**")
                    for o in sorted(home_odds, key=lambda x: x['odd'], reverse=True)[:3]:
                        st.write(f"{o['casa']}: **{o['odd']}**")
                with col2:
                    st.markdown("**EMPATE**")
                    for o in sorted(draw_odds, key=lambda x: x['odd'], reverse=True)[:3]:
                        st.write(f"{o['casa']}: **{o['odd']}**")
                with col3:
                    st.markdown("**FORA**")
                    for o in sorted(away_odds, key=lambda x: x['odd'], reverse=True)[:3]:
                        st.write(f"{o['casa']}: **{o['odd']}**")
        
        # ESTATÍSTICAS DE GOLS
        if pred:
            teams_data = pred.get('teams', {})
            home_data = teams_data.get('home', {}).get('league', {}).get('goals', {})
            away_data = teams_data.get('away', {}).get('league', {}).get('goals', {})
            
            if home_data and away_data:
                st.markdown("### ⚽ MÉDIAS DE GOLS")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**{jogo['teams']['home']['name']}**")
                    gf = home_data.get('for', {}).get('average', {}).get('total', '-')
                    ga = home_data.get('against', {}).get('average', {}).get('total', '-')
                    st.write(f"🟢 Feitos: {gf}/jogo")
                    st.write(f"🔴 Sofridos: {ga}/jogo")
                with col2:
                    st.markdown(f"**{jogo['teams']['away']['name']}**")
                    gf = away_data.get('for', {}).get('average', {}).get('total', '-')
                    ga = away_data.get('against', {}).get('average', {}).get('total', '-')
                    st.write(f"🟢 Feitos: {gf}/jogo")
                    st.write(f"🔴 Sofridos: {ga}/jogo")
        
        # H2H
        if pred and pred.get('h2h'):
            st.markdown("### 🔄 H2H")
            for h in pred['h2h'][:5]:
                home = h['teams']['home']['name']
                away = h['teams']['away']['name']
                gh = h['goals']['home']
                ga = h['goals']['away']
                data = h['fixture']['date'][:10]
                st.write(f"📅 {data} | {home} {gh}-{ga} {away}")

# ============================================
# TAB 4: HISTÓRICO E GESTÃO
# ============================================
with tab4:
    st.markdown("### 📋 HISTÓRICO DE APOSTAS")
    
    # Estatísticas gerais
    stats = calcular_estatisticas()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total", stats['total'])
    with col2:
        st.metric("✅ Ganhas", stats['ganhas'])
    with col3:
        st.metric("❌ Perdidas", stats['perdidas'])
    with col4:
        st.metric("💰 Cashouts", stats['cashouts'])
    with col5:
        st.metric("⏳ Pendentes", stats['pendentes'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        cor = "normal" if stats['roi'] >= 0 else "inverse"
        st.metric("ROI", f"{stats['roi']}%", delta=f"{stats['roi']}%", delta_color=cor)
    with col2:
        cor = "normal" if stats['lucro_total'] >= 0 else "inverse"
        st.metric("Lucro/Prejuízo", f"R$ {stats['lucro_total']}", delta_color=cor)
    with col3:
        st.metric("Taxa de Acerto", f"{stats['taxa_acerto']}%")
    
    st.markdown("---")
    
    # Lista de apostas pendentes
    pendentes = [a for a in st.session_state['historico_apostas'] if a['status'] == 'pendente']
    
    if pendentes:
        st.markdown("### ⏳ APOSTAS PENDENTES")
        
        for aposta in pendentes:
            with st.expander(f"#{aposta['id']} | {aposta['jogo']} | {aposta['selecao']} @ {aposta['odd']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Mercado:** {aposta['mercado']}")
                    st.write(f"**Casa:** {aposta['casa']}")
                with col2:
                    st.write(f"**Stake:** R$ {aposta['stake']:.2f}")
                    st.write(f"**Retorno Potencial:** R$ {aposta['stake'] * aposta['odd']:.2f}")
                with col3:
                    st.write(f"**Data:** {aposta['data']}")
                
                st.markdown("**Marcar resultado:**")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("✅ GANHOU", key=f"ganhou_{aposta['id']}"):
                        atualizar_resultado(aposta['id'], 'ganhou')
                        st.rerun()
                with col2:
                    if st.button("❌ PERDEU", key=f"perdeu_{aposta['id']}"):
                        atualizar_resultado(aposta['id'], 'perdeu')
                        st.rerun()
                with col3:
                    cashout_val = st.number_input("Valor:", min_value=0.0, value=aposta['stake'], key=f"cash_{aposta['id']}")
                    if st.button("💰 CASHOUT", key=f"cashout_{aposta['id']}"):
                        atualizar_resultado(aposta['id'], 'cashout', cashout_val)
                        st.rerun()
                with col4:
                    if st.button("🔄 VOID", key=f"void_{aposta['id']}"):
                        atualizar_resultado(aposta['id'], 'void')
                        st.rerun()
    
    st.markdown("---")
    
    # Histórico completo
    st.markdown("### 📜 HISTÓRICO COMPLETO")
    
    finalizadas = [a for a in st.session_state['historico_apostas'] if a['status'] != 'pendente']
    finalizadas.reverse()  # Mais recentes primeiro
    
    if finalizadas:
        for aposta in finalizadas:
            status_emoji = {'ganhou': '✅', 'perdeu': '❌', 'cashout': '💰', 'void': '🔄'}
            status_cor = {'ganhou': '#4ade80', 'perdeu': '#f87171', 'cashout': '#fbbf24', 'void': '#888'}
            lucro_cor = '#4ade80' if aposta['lucro'] >= 0 else '#f87171'
            
            st.markdown(f"""
            <div style="background: #1a1a1a; border-left: 4px solid {status_cor[aposta['status']]}; padding: 10px; margin: 5px 0; border-radius: 4px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{status_emoji[aposta['status']]} #{aposta['id']}</strong> | {aposta['jogo']}<br>
                        <small style="color: #888;">{aposta['selecao']} @ {aposta['odd']} | {aposta['casa']} | {aposta['data']}</small>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #888;">Stake: R$ {aposta['stake']:.2f}</div>
                        <div style="color: {lucro_cor}; font-weight: bold;">
                            {'+' if aposta['lucro'] >= 0 else ''}R$ {aposta['lucro']:.2f}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhuma aposta finalizada ainda.")
    
    # Opções de gestão
    st.markdown("---")
    st.markdown("### ⚙️ GESTÃO")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ LIMPAR HISTÓRICO", type="secondary"):
            st.session_state['historico_apostas'] = []
            st.success("Histórico limpo!")
            st.rerun()
    with col2:
        # Recarregar banca da reserva
        valor_recarregar = st.number_input("Transferir da reserva:", min_value=0.0, max_value=st.session_state['reserva'], value=0.0)
        if st.button("💸 TRANSFERIR PARA BANCA"):
            if valor_recarregar > 0 and valor_recarregar <= st.session_state['reserva']:
                st.session_state['reserva'] -= valor_recarregar
                st.session_state['banca_ativa'] += valor_recarregar
                st.success(f"R$ {valor_recarregar:.2f} transferido para banca ativa!")
                st.rerun()
