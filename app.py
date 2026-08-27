import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(
    page_title="Finan-ass | Dashboard Financeiro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada (Dark Mode & Cards)
st.markdown("""
    <style>
    .main { background-color: #121417; }
    .stApp { background-color: #121417; color: #FFFFFF; }
    div[data-testid="metric-container"] {
        background-color: #1E222A;
        border: 1px solid #2D333F;
        padding: 15px;
        border-radius: 10px;
    }
    .stButton>button {
        width: 100%;
        background-color: #00C853;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #00E676;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Barra Lateral (Sidebar)
st.sidebar.title("📊 Finan-ass")
st.sidebar.subheader("Painel de Controle")

ticker = st.sidebar.text_input("Ativo", value="PETR4.SA").upper()

periodos = {
    "1 Dia": "1d",
    "1 Mês": "1mo",
    "6 Meses": "6mo",
    "1 Ano": "1y",
    "5 Anos": "5y"
}
periodo_nome = st.sidebar.selectbox("Período", list(periodos.keys()), index=2)
periodo_sel = periodos[periodo_nome]

buscar = st.sidebar.button("BUSCAR DADOS")

# Título Principal
st.title("📈 ANÁLISE FINANCEIRA AVANÇADA EM TEMPO REAL")
st.caption("Dashboard de monitoramento de ativos com indicadores técnicos e volume.")

# Lógica de Busca e Renderização
if buscar or ticker:
    with st.spinner("Buscando dados em tempo real..."):
        # Ajuste de intervalo para dados intraday (1 Dia)
        intervalo = "15m" if periodo_sel == "1d" else "1d"
        dados = yf.download(ticker, period=periodo_sel, interval=intervalo)
        
        if not dados.empty:
            # Correção de MultiIndex de colunas se retornado pelo yfinance
            if isinstance(dados.columns, pd.MultiIndex):
                dados.columns = dados.columns.get_level_values(0)

            # Cálculo de Médias Móveis
            dados['MMA20'] = dados['Close'].rolling(window=20).mean()
            dados['MMA50'] = dados['Close'].rolling(window=50).mean()

            # Extração dos valores para os Cards
            preco_atual = dados['Close'].iloc[-1]
            preco_anterior = dados['Close'].iloc[-2] if len(dados) > 1 else preco_atual
            variacao = preco_atual - preco_anterior
            var_percentual = (variacao / preco_anterior) * 100
            
            maxima = dados['High'].max()
            minima = dados['Low'].min()

            # Layout de Cards Topo (Métricas)
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Ativo Selecionado", ticker)
            col2.metric("Preço Atual", f"R$ {preco_atual:.2f}", f"{var_percentual:+.2f}%")
            col3.metric(f"Máxima ({periodo_nome})", f"R$ {maxima:.2f}")
            col4.metric(f"Mínima ({periodo_nome})", f"R$ {minima:.2f}")

            st.divider()

            # Criação do Gráfico Duplo (Candlestick + Volume)
            fig = make_subplots(
                rows=2, cols=1, 
                shared_xaxes=True, 
                vertical_spacing=0.03, 
                row_heights=[0.7, 0.3]
            )

            # Candlestick
            fig.add_trace(go.Candlestick(
                x=dados.index,
                open=dados['Open'],
                high=dados['High'],
                low=dados['Low'],
                close=dados['Close'],
                name="Candles"
            ), row=1, col=1)

            # Médias Móveis
            fig.add_trace(go.Scatter(
                x=dados.index, y=dados['MMA20'], 
                line=dict(color='#29b6f6', width=1.5), 
                name="MMA 20"
            ), row=1, col=1)

            fig.add_trace(go.Scatter(
                x=dados.index, y=dados['MMA50'], 
                line=dict(color='#ffb74d', width=1.5), 
                name="MMA 50"
            ), row=1, col=1)

            # Volume
            fig.add_trace(go.Bar(
                x=dados.index, y=dados['Volume'], 
                marker_color='#5c6bc0', 
                name="Volume"
            ), row=2, col=1)

            # Layout Dark do Gráfico
            fig.update_layout(
                title=f"Histórico de Preços e Indicadores: {ticker} ({periodo_nome})",
                template="plotly_dark",
                xaxis_rangeslider_visible=False,
                height=550,
                paper_bgcolor="#1E222A",
                plot_bgcolor="#1E222A",
                margin=dict(l=20, r=20, t=40, b=20)
            )

            st.plotly_chart(fig, use_container_width=True)

            # Tabela de Dados Recentes
            with st.expander("📋 Ver tabela de dados detalhados"):
                st.dataframe(dados.tail(10), use_container_width=True)
        else:
            st.error("Não foi possível carregar os dados. Verifique se o código do ativo está correto.")