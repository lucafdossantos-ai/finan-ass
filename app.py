import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Análise Financeira", layout="wide")

st.title("📈 Análise do Mercado Financeiro em Tempo Real")

# Barra lateral para entrada de dados
st.sidebar.header("Configurações")
ticker = st.sidebar.text_input("Código do Ativo (ex: PETR4.SA, VALE3.SA, AAPL):", value="PETR4.SA")

periodos = {"1 Mês": "1mo", "6 Meses": "6mo", "1 Ano": "1y", "5 Anos": "5y"}
periodo_sel = st.sidebar.selectbox("Período:", list(periodos.keys()))

if st.sidebar.button("Buscar Dados"):
    with st.spinner("Carregando cotações..."):
        dados = yf.download(ticker, period=periodos[periodo_sel])
        
        if not dados.empty:
            st.subheader(f"Histórico de Preços - {ticker.upper()}")
            
            # Gráfico de Candlestick
            fig = go.Figure(data=[go.Candlestick(
                x=dados.index,
                open=dados['Open'],
                high=dados['High'],
                low=dados['Low'],
                close=dados['Close']
            )])
            fig.update_layout(xaxis_rangeslider_visible=False, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela com últimos registros
            st.subheader("Dados Recentes")
            st.dataframe(dados.tail())
        else:
            st.error("Nenhum dado encontrado para o ticker informado. Verifique o código do ativo.")