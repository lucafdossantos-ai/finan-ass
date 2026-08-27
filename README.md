# 📈 Dashboard de Análise Financeira Avançada em Tempo Real

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly" />
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
</p>

> Uma aplicação interativa web para monitoramento e análise técnica do mercado financeiro em tempo real, construída em Python com **Streamlit**, **Yahoo Finance** e **Plotly**.

---

## 🌐 Acesse a Aplicação Online

Acesse o dashboard ao vivo publicado no Streamlit Cloud:  
👉 **[Clique aqui para abrir o Finan-ass no Streamlit Cloud](https://share.streamlit.io/)** *(Substitua este link pelo link direto da sua aplicação)*

---

## 🖥️ Demonstração da Interface

![Dashboard Financial Preview](https://raw.githubusercontent.com/lucafdossantos-ai/finan-ass/main/preview.png)
*(Dica: Adicione uma captura de tela do seu app na pasta do repositório com o nome `preview.png`)*

---

## 🎯 Principais Funcionalidades

- 📊 **Cotações em Tempo Real:** Consulta automatizada de ativos brasileiros (B3) e globais via API do Yahoo Finance.
- 📉 **Gráficos Interativos (Candlestick):** Visualização dinâmica alimentada por `Plotly`.
- 📐 **Indicadores Técnicos:**
  - Média Móvel Simples (MMA 20)
  - Média Móvel Simples (MMA 50)
- 📦 **Volume de Negociação:** Subgráfico de volume sincronizado com o preço do ativo.
- 🎛️ **Controle de Períodos:** Seleção flexível de intervalos de tempo (1 Dia, 1 Mês, 6 Meses, 1 Ano, 5 Anos).
- 🏷️ **Cards de Resumo (KPIs):** Exibição instantânea do Preço Atual, Variação %, Máxima e Mínima do período.
- 📋 **Tabela de Dados:** Extrator de dados históricos recentes para auditoria rápida.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Descrição |
| :--- | :--- |
| **Python** | Linguagem principal do projeto |
| **Streamlit** | Framework para criação da interface web interativa |
| **yfinance** | Biblioteca para consumo de dados da API do Yahoo Finance |
| **Plotly** | Renderização de gráficos financeiros interativos avançados |
| **Pandas** | Manipulação e cálculo de séries temporais / indicadores |

---

## 🚀 Como Executar o Projeto Localmente

Se desejar executar este projeto em sua máquina local:

### 1. Clonar o repositório
```bash
git clone [https://github.com/lucafdossantos-ai/finan-ass.git](https://github.com/lucafdossantos-ai/finan-ass.git)
cd finan-ass
