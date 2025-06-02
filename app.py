import streamlit as st

# Configuração da página do Streamlit
# MOVER st.set_page_config PARA O TOPO, LOGO APÓS 'import streamlit as st'
st.set_page_config(
    layout="wide",
    page_title="Bolsa de Valores do Brasil",
    page_icon="📉",
    initial_sidebar_state="collapsed",
)

import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import datetime as dt
from streamlit_extras.metric_cards import style_metric_cards

# Bootstrap
st.markdown(
    """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
<link href="style.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
""",
    unsafe_allow_html=True,
)


# Configuração inicial do Streamlit
st.title("Análise de Ações da Bolsa de Valores do Brasil")
st.subheader("Selecione uma ação, data de início e data de fim:")


# Lista de ações da bolsa do Brasil
acoes = [
    "ABEV3.SA",
    "AZUL4.SA",
    "B3SA3.SA",
    "BBAS3.SA",
    "BBDC3.SA",
    "BBDC4.SA",
    "BBSE3.SA",
    "BEEF3.SA",
    "BPAC11.SA",
    "BRAP4.SA",
    "BRDT3.SA",
    "BRFS3.SA",
    "BRKM5.SA",
    "BRML3.SA",
    "BTOW3.SA",
    "CCRO3.SA",
    "CIEL3.SA",
    "CMIG4.SA",
    "COGN3.SA",
    "CPFE3.SA",
    "CRFB3.SA",
    "CSAN3.SA",
    "CSNA3.SA",
    "CVCB3.SA",
    "CYRE3.SA",
    "ECOR3.SA",
    "EGIE3.SA",
    "ELET3.SA",
    "ELET6.SA",
    "EMBR3.SA",
    "ENBR3.SA",
    "ENGI11.SA",
    "EQTL3.SA",
    "FLRY3.SA",
    "GGBR4.SA",
    "GNDI3.SA",
    "GOAU4.SA",
    "GOLL4.SA",
    "HAPV3.SA",
    "HGTX3.SA",
    "HYPE3.SA",
    "IGTA3.SA",
    "IRBR3.SA",
    "ITSA4.SA",
    "ITUB4.SA",
    "JBSS3.SA",
    "JHSF3.SA",
    "KLBN11.SA",
    "LAME4.SA",
    "LCAM3.SA",
    "LREN3.SA",
    "MGLU3.SA",
    "MRFG3.SA",
    "MRVE3.SA",
    "MULT3.SA",
    "NTCO3.SA",
    "PCAR3.SA",
    "PETR3.SA",
    "PETR4.SA",
    "QUAL3.SA",
    "RADL3.SA",
    "RAIL3.SA",
    "RENT3.SA",
    "SANB11.SA",
    "SBSP3.SA",
    "SULA11.SA",
    "SUZB3.SA",
    "TAEE11.SA",
    "TIMP3.SA",
    "TOTS3.SA",
    "UGPA3.SA",
    "USIM5.SA",
    "VALE3.SA",
    "VIVT3.SA",
    "VVAR3.SA",
    "WEGE3.SA",
    "YDUQ3.SA",
]

# Datas de início e fim
end_date = dt.datetime.today()
start_date = dt.datetime(end_date.year - 1, end_date.month, end_date.day)

# Criando o container de interação com o usuário
with st.container():
    # Criando 3 colunas
    col1, col2, col3 = st.columns(3)

    with col1:
        # Dropdown com as ações
        acao = st.selectbox("Selecione o ativo do seu interesse:", acoes)

    with col2:
        # Seleção da data de início e fim
        data_inicio = st.date_input("Data de início:", start_date)

    with col3:
        data_fim = st.date_input("Data de fim:", end_date)

# espaço entre as linhas

st.markdown("#")

# Obtendo os dados da ação selecionada
dados = yf.download(acao, start=data_inicio, end=data_fim)

# Verificar se 'dados' está vazio e parar a execução se necessário
if dados.empty:
    st.error(f"Não foram encontrados dados para o ativo {acao} no período de {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}.")
    st.stop()


# Métricas
ult_atualizacao = dados.index.max().strftime("%d/%m/%Y")  # Data da última atualização
ult_cotacao = round(
    dados["Close"].iloc[-1].item(), 2  # Garante que é um escalar antes de arredondar
)  # última cotação encontrada
menor_cotacao = round(dados["Close"].min().item(), 2)  # Garante que é um escalar
maior_cotacao = round(dados["Close"].max().item(), 2)  # Garante que é um escalar
primeira_cotacao = round(
    dados["Close"].iloc[0].item(), 2  # Garante que é um escalar antes de arredondar
)  # Primeira cotação do período
delta = round(
    ((ult_cotacao - primeira_cotacao) / primeira_cotacao) * 100, 2
)  # Delta da cotação
volume_total = dados["Volume"].sum().item()  # Garante que é um escalar
var_menor_cotacao = round(
    ((menor_cotacao - primeira_cotacao) / primeira_cotacao) * 100, 2
)
var_maior_cotacao = round(
    ((maior_cotacao - primeira_cotacao) / primeira_cotacao) * 100, 2
)

# Colunas de métricas
col4, col5, col6, col7 = st.columns(4)


style_metric_cards(
    background_color="#46629e", border_left_color="#68ba9f", border_color="#68ba9f"
)


with col4:
    st.metric(
        label="Último Preço",
        value="R$ {:,.2f}".format(ult_cotacao),
        delta="{}%".format(delta),
    )


with col5:
    st.metric(
        label=":red[Menor Cotação do período]",
        value="R$ {:,.2f}".format(menor_cotacao),
        delta="{}%  -  Relação ao valor inicial".format(var_menor_cotacao),
    )


with col6:
    st.metric(
        label=":green[Maior Cotação do período]",
        value="R$ {:,.2f}".format(maior_cotacao),
        delta="{}%  -  Relação ao valor inicial".format(var_maior_cotacao),
    )


with col7:
    st.metric(
        label=":orange[Volume Total no Período]",
        value="{:,.2f}".format(volume_total),
        delta="_",
    )

# Adiciona um espaço em branco para alinhar os cards
st.markdown("<br>", unsafe_allow_html=True)


# Coluna Date no formato %d/%m/%Y
dados.index = dados.index.strftime("%d/%m/%Y")

with st.container():
    col8, col9 = st.columns([1.5, 3], gap="large")

    with col8:
        # Exibindo os dados da ação
        st.markdown(
            "<h4 style='text-align: center;'>Principais valores do ativo</h4>",
            unsafe_allow_html=True,
        )
        st.dataframe(dados, use_container_width=True)

    # Gráfico de area
    with col9:
        # Verificando se há dados disponíveis para a ação selecionada
        if dados.empty:
            st.write("Não há dados disponíveis para a ação selecionada.")
        else:
            # Gráfico de área com os preços
            fig_area = go.Figure(
                data=go.Scatter(
                    x=dados.index,
                    y=dados["Close"], # Alterado de "Adj Close" para "Close"
                    fill="tozerox",
                )
            )
            fig_area.update_layout(
                title="Evolução dos preços no período",
                xaxis_title="Data",
                yaxis_title="Preço Ajustado",
                title_x=0.5,
                hovermode="closest",
                height=600,
            )
            st.plotly_chart(fig_area, use_container_width=True)

# Adiciona um espaço em branco
st.markdown("<br>", unsafe_allow_html=True)

# Gráfico de candlestick
with st.container():

    fig_candlestick = go.Figure(
        data=go.Candlestick(
            x=dados.index,
            open=dados["Open"],
            high=dados["High"],
            low=dados["Low"],
            close=dados["Close"],
        )
    )
    fig_candlestick.update_layout(
        title="Candlesticks Diários",
        title_font_size=20,
        xaxis_title="Data",
        yaxis_title="Preço",
        height=800,
        title_x=0.5,
        xaxis_rangeslider_visible=False,
    )

    st.plotly_chart(fig_candlestick, use_container_width=True)
