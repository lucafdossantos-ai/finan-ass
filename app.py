import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Finan-ass | Terminal Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS Avançada
st.markdown("""
    <style>
    .stApp {
        background-color: #0B0E14;
        color: #E6E8EA;
    }
    
    #MainMenu, footer, header {visibility: hidden;}

    /* Inputs e Formulário */
    div[data-baseweb="input"] {
        background-color: #161B22 !important;
        border-color: #30363D !important;
        border-radius: 8px !important;
    }
    
    div[data-baseweb="input"] input {
        color: #00E676 !important;
        font-weight: bold !important;
    }

    /* Cards de Métricas */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Botão Principal */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #00C853 0%, #00E676 100%);
        color: #000000 !important;
        font-weight: 800;
        border: none;
        border-radius: 8px;
        padding: 12px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(0, 230, 118, 0.4);
        transform: translateY(-1px);
    }

    /* Card de Notícias */
    .news-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .news-title {
        color: #00E676;
        font-weight: bold;
        text-decoration: none;
        font-size: 15px;
    }
    .news-publisher {
        color: #8B949E;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE CACHE PARAN OTIMIZAÇÃO ---
@st.cache_data(ttl=300, show_spinner=False)
def buscar_dados_historicos(ticker, periodo, intervalo):
    return yf.download(ticker, period=periodo, interval=intervalo)

@st.cache_data(ttl=600, show_spinner=False)
def buscar_info_ticker(ticker):
    try:
        t = yf.Ticker(ticker)
        return t.info, t.news
    except Exception:
        return {}, []

# --- BASE DE DADOS GLOBAL ---
TOP_EMPRESAS_GLOBAIS = {
    "🇧🇷 Brasil (B3)": {
        "VALE3.SA": "Vale S.A.", "PETR4.SA": "Petrobras (PN)", "ITUB4.SA": "Itaú Unibanco",
        "BBDC4.SA": "Banco Bradesco", "BBAS3.SA": "Banco do Brasil", "ABEV3.SA": "Ambev S.A.",
        "WEGE3.SA": "WEG S.A.", "RENT3.SA": "Localiza Rent a Car", "B3SA3.SA": "B3 S.A.",
        "SUZB3.SA": "Suzano S.A.", "JBSS3.SA": "JBS S.A.", "GGBR4.SA": "Gerdau S.A.",
        "PRIO3.SA": "Prio (PetroRio)", "BPAC11.SA": "BTG Pactual", "EQTL3.SA": "Equatorial Energia",
        "LREN3.SA": "Lojas Renner", "RADL3.SA": "Raia Drogasil", "ELET3.SA": "Eletrobras",
        "VBBR3.SA": "Vibra Energia", "CSAN3.SA": "Cosan S.A."
    },
    "🇺🇸 Estados Unidos (Wall St)": {
        "NVDA": "NVIDIA Corporation", "AAPL": "Apple Inc.", "MSFT": "Microsoft Corporation",
        "AMZN": "Amazon.com Inc.", "GOOGL": "Alphabet Inc. (Google)", "META": "Meta Platforms",
        "TSLA": "Tesla, Inc.", "BRK-B": "Berkshire Hathaway", "AVGO": "Broadcom Inc.",
        "JNJ": "Johnson & Johnson", "JPM": "JPMorgan Chase", "WMT": "Walmart Inc.",
        "V": "Visa Inc.", "PG": "Procter & Gamble", "UNH": "UnitedHealth Group",
        "MA": "Mastercard Inc.", "HD": "Home Depot", "NFLX": "Netflix, Inc.",
        "COST": "Costco Wholesale", "ABBV": "AbbVie Inc."
    },
    "🇩🇪 Alemanha (DAX)": {
        "SAP.DE": "SAP SE", "SIE.DE": "Siemens AG", "ALV.DE": "Allianz SE",
        "AIR.DE": "Airbus SE", "DTE.DE": "Deutsche Telekom", "MBG.DE": "Mercedes-Benz Group"
    },
    "🇬🇧 Reino Unido (FTSE)": {
        "SHEL.L": "Shell plc", "AZN.L": "AstraZeneca plc", "HSBA.L": "HSBC Holdings",
        "ULVR.L": "Unilever PLC", "BP.L": "BP plc"
    },
    "🇫🇷 França (CAC 40)": {
        "MC.PA": "LVMH Moët Hennessy", "TTE.PA": "TotalEnergies SE", "RMS.PA": "Hermès International",
        "OR.PA": "L'Oréal S.A.", "SAN.PA": "Sanofi"
    },
    "🇯🇵 Japão (Nikkei/TOPIX)": {
        "7203.T": "Toyota Motor", "6758.T": "Sony Group", "8306.T": "Mitsubishi UFJ Financial"
    },
    "🇨🇳 China / Hong Kong": {
        "0700.HK": "Tencent Holdings", "9988.HK": "Alibaba Group", "3690.HK": "Meituan"
    }
}

def obter_nome_empresa(ticker_codigo, info):
    for pais, empresas in TOP_EMPRESAS_GLOBAIS.items():
        if ticker_codigo in empresas:
            return empresas[ticker_codigo]
    return info.get('longName') or info.get('shortName') or ticker_codigo

def formatar_numero(valor):
    if not valor or pd.isna(valor):
        return "N/A"
    if valor >= 1e12:
        return f"{valor/1e12:.2f}T"
    if valor >= 1e9:
        return f"{valor/1e9:.2f}B"
    if valor >= 1e6:
        return f"{valor/1e6:.2f}M"
    return f"{valor:,.2f}"

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.markdown("## ⚡ **FINAN-ASS PRO**")
st.sidebar.caption("Terminal Analítico de Ativos Globais")

st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Top Empresas Globais")

pais_selecionado = st.sidebar.selectbox("Escolha o País / Região", list(TOP_EMPRESAS_GLOBAIS.keys()))
empresas_do_pais = TOP_EMPRESAS_GLOBAIS[pais_selecionado]

empresa_preselecionada = st.sidebar.selectbox(
    "Selecione uma Empresa do Filtro", 
    options=list(empresas_do_pais.keys()),
    format_func=lambda x: f"{empresas_do_pais[x]} ({x})"
)

with st.sidebar.form(key="search_form"):
    ticker_input = st.text_input("Ou Digite o Código Manualmente", value=empresa_preselecionada)
    
    periodos = {
        "1 Dia": "1d",
        "1 Mês": "1mo",
        "6 Meses": "6mo",
        "1 Ano": "1y",
        "5 Anos": "5y"
    }
    periodo_nome = st.selectbox("Intervalo Temporal", list(periodos.keys()), index=2)
    
    btn_buscar = st.form_submit_button("PESQUISAR ATIVO 🔍")

ticker = ticker_input.strip().upper()
if not ticker.endswith(".SA") and len(ticker) <= 6 and ticker.endswith(("3", "4", "11")) and not "." in ticker:
    ticker += ".SA"

periodo_sel = periodos[periodo_nome]

st.sidebar.markdown("---")
st.sidebar.subheader("Indicadores Técnicos")
exibir_bollinger = st.sidebar.checkbox("Bandas de Bollinger", value=True)
exibir_rsi = st.sidebar.checkbox("Exibir RSI / IFR", value=True)

# --- PROCESSAMENTO DE DADOS ---
if ticker:
    with st.spinner(f"Buscando dados de {ticker}..."):
        intervalo = "15m" if periodo_sel == "1d" else "1d"
        dados = buscar_dados_historicos(ticker, periodo_sel, intervalo)
        info_ticker, noticias_ticker = buscar_info_ticker(ticker)
        
        nome_empresa = obter_nome_empresa(ticker, info_ticker)

        # CABEÇALHO
        st.title("⚡ TERMINAL DE ANÁLISE COMPLETA")
        st.caption(f"Exibindo dados dinâmicos para: **{nome_empresa}** (`{ticker}`)")

        if not dados.empty:
            if isinstance(dados.columns, pd.MultiIndex):
                dados.columns = dados.columns.get_level_values(0)

            # Cálculo Técnicos
            dados['MMA20'] = dados['Close'].rolling(window=20).mean()
            dados['MMA50'] = dados['Close'].rolling(window=50).mean()

            std = dados['Close'].rolling(window=20).std()
            dados['Boll_Upper'] = dados['MMA20'] + (std * 2)
            dados['Boll_Lower'] = dados['MMA20'] - (std * 2)

            delta = dados['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            dados['RSI'] = 100 - (100 / (1 + rs))

            # Preço e Variação
            preco_atual = dados['Close'].iloc[-1]
            preco_anterior = dados['Close'].iloc[-2] if len(dados) > 1 else preco_atual
            variacao = preco_atual - preco_anterior
            var_percentual = (variacao / preco_anterior) * 100
            minima = dados['Low'].min()

            # --- BLOCO 1: KPIs DE MERCADO ---
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Empresa / Ativo", nome_empresa, ticker)
            c2.metric("Preço Atual", f"R$ {preco_atual:.2f}" if ticker.endswith(".SA") else f"$ {preco_atual:.2f}", f"{var_percentual:+.2f}%")
            c3.metric(f"Máxima ({periodo_nome})", f"{dados['High'].max():.2f}")
            c4.metric(f"Mínima ({periodo_nome})", f"{minima:.2f}")

            # --- BLOCO 2: INDICADORES FUNDAMENTALISTAS ---
            st.markdown("### 📊 Indicadores Fundamentalistas")
            f1, f2, f3, f4, f5 = st.columns(5)
            
            pe_ratio = info_ticker.get('trailingPE')
            pb_ratio = info_ticker.get('priceToBook')
            dy = info_ticker.get('dividendYield')
            market_cap = info_ticker.get('marketCap')
            roe = info_ticker.get('returnOnEquity')

            f1.metric("P/L (Preço/Lucro)", f"{pe_ratio:.2f}" if pe_ratio else "N/A")
            f2.metric("P/VP", f"{pb_ratio:.2f}" if pb_ratio else "N/A")
            f3.metric("Dividend Yield", f"{dy*100:.2f}%" if dy else "N/A")
            f4.metric("Valor de Mercado", formatar_numero(market_cap))
            f5.metric("ROE", f"{roe*100:.2f}%" if roe else "N/A")

            st.markdown("<br>", unsafe_allow_html=True)

            # --- BLOCO 3: GRÁFICO TÉCNICO ---
            num_rows = 3 if exibir_rsi else 2
            row_heights = [0.6, 0.2, 0.2] if exibir_rsi else [0.75, 0.25]

            fig = make_subplots(
                rows=num_rows, cols=1, 
                shared_xaxes=True, 
                vertical_spacing=0.03, 
                row_heights=row_heights
            )

            fig.add_trace(go.Candlestick(
                x=dados.index, open=dados['Open'], high=dados['High'],
                low=dados['Low'], close=dados['Close'], name="Preço"
            ), row=1, col=1)

            fig.add_trace(go.Scatter(x=dados.index, y=dados['MMA20'], line=dict(color='#00E5FF', width=1.2), name="MMA 20"), row=1, col=1)
            fig.add_trace(go.Scatter(x=dados.index, y=dados['MMA50'], line=dict(color='#FFD600', width=1.2), name="MMA 50"), row=1, col=1)

            if exibir_bollinger:
                fig.add_trace(go.Scatter(x=dados.index, y=dados['Boll_Upper'], line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dot'), name="Boll Sup"), row=1, col=1)
                fig.add_trace(go.Scatter(x=dados.index, y=dados['Boll_Lower'], line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dot'), fill='tonexty', fillcolor='rgba(255,255,255,0.03)', name="Boll Inf"), row=1, col=1)

            cores_vol = ['#00E676' if c >= o else '#FF5252' for c, o in zip(dados['Close'], dados['Open'])]
            fig.add_trace(go.Bar(x=dados.index, y=dados['Volume'], marker_color=cores_vol, name="Volume"), row=2, col=1)

            if exibir_rsi:
                fig.add_trace(go.Scatter(x=dados.index, y=dados['RSI'], line=dict(color='#AB47BC', width=1.5), name="RSI (14)"), row=3, col=1)
                fig.add_hline(y=70, line_dash="dash", line_color="#FF5252", row=3, col=1, opacity=0.5)
                fig.add_hline(y=30, line_dash="dash", line_color="#00E676", row=3, col=1, opacity=0.5)

            fig.update_layout(
                title=f"Histórico e Indicadores: {nome_empresa} ({ticker})",
                template="plotly_dark",
                xaxis_rangeslider_visible=False,
                height=650,
                paper_bgcolor="#161B22",
                plot_bgcolor="#161B22",
                margin=dict(l=15, r=15, t=40, b=15),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )

            st.plotly_chart(fig, use_container_width=True)

            # --- BLOCO 4: NOTÍCIAS E DADOS BRUTOS ---
            col_noticias, col_dados = st.columns([1, 1])

            with col_noticias:
                st.markdown("### 📰 ÚLTIMAS NOTÍCIAS")
                if noticias_ticker:
                    for item in noticias_ticker[:4]:
                        titulo = item.get('title')
                        link = item.get('link')
                        publisher = item.get('publisher', 'Fonte Desconhecida')
                        
                        st.markdown(f"""
                        <div class="news-card">
                            <a href="{link}" target="_blank" class="news-title">{titulo}</a>
                            <div class="news-publisher">Fonte: {publisher}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Nenhuma notícia recente encontrada para este ativo.")

            with col_dados:
                st.markdown("### 📋 DADOS HISTÓRICOS")
                st.dataframe(dados.sort_index(ascending=False), use_container_width=True, height=280)

        else:
            st.error(f"Erro ao buscar '{ticker}'. Verifique a digitação do código do ativo.")