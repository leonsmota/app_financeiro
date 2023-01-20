import streamlit as st
import pandas as pd
import yfinance as yf
import investpy as inv
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date
import sys
import plotly.graph_objects as go
import fundamentus as fd

def home():
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image('masqueico.jpeg', width=200)
        st.markdown('---')
        st.title('App Financeiro')
        st.markdown('---')

def panorama():
    st.title('Panorama do Mercado')
    st.markdown(date.today().strftime('%d/%m/%Y'))

    st.subheader('Mercados pelo Mundo')

    dict_tickers = {
                'Bovespa':'^BVSP',
                'S&P500':'^GSPC',
                'NASDAQ':'^IXIC',
                'DAX':'^GDAXI',
                'FISE 100':'^FTSE',
                'Cruid Oil':'CL=F',
                'Gold':'GC=F',
                'Bitcoin':'BTC-USD',
                'Etherium':'ETH-USD'
                 }

    df_info = pd.DataFrame({'Ativo': dict_tickers.keys(), 'Ticker': dict_tickers.values()})

    df_info['Ult. Valor'] = ''
    df_info['%'] = ''
    count = 0
    print('teste ' * 10)
    with st.spinner('Baixando Cotações...'):
        for ticker in dict_tickers.values():
            lines = str(yf.download(ticker, period='2d')['Close']).split('\n')
            v1 = float(lines[1].split(' ')[-1])

            try:
                v2 = float(lines[2].split(' ')[-1])
                # print(cotacoes)
                variacao = ((v2 / v1) - 1) * 100
                # variacao = ((cotacoes.iloc[-1] / cotacoes.iloc[-2]) - 1) * 100

                df_info['Ult. Valor'][count] = round(v2, 2)
                # df_info['Ult. Valor'][count] = round(cotacoes.iloc[-1], 2)
                df_info['%'][count] = round(variacao, 2)
                count += 1
            except:
                pass
        st.write(df_info)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(df_info['Ativo'][0], value=df_info['Ult. Valor'][0], delta=str(df_info['%'][0]) + '%')
        st.metric(df_info['Ativo'][1], value=df_info['Ult. Valor'][1], delta=str(df_info['%'][1]) + '%')
        st.metric(df_info['Ativo'][2], value=df_info['Ult. Valor'][2], delta=str(df_info['%'][2]) + '%')

    with col2:
        st.metric(df_info['Ativo'][3], value=df_info['Ult. Valor'][3], delta=str(df_info['%'][3]) + '%')
        st.metric(df_info['Ativo'][4], value=df_info['Ult. Valor'][4], delta=str(df_info['%'][4]) + '%')
        st.metric(df_info['Ativo'][5], value=df_info['Ult. Valor'][5], delta=str(df_info['%'][5]) + '%')

    with col3:
        st.metric(df_info['Ativo'][6], value=df_info['Ult. Valor'][6], delta=str(df_info['%'][6]) + '%')
        st.metric(df_info['Ativo'][7], value=df_info['Ult. Valor'][7], delta=str(df_info['%'][7]) + '%')
        st.metric(df_info['Ativo'][8], value=df_info['Ult. Valor'][8], delta=str(df_info['%'][8]) + '%')

    st.markdown('---')

    st.subheader('Comportamento durante o dia')

    lista_indices = ['IBOV', 'S&P500', 'NASDAQ']

    indice = st.selectbox('Selecione o Índice', lista_indices)

    if indice == 'IBOV':
        indice_diario = yf.download('^BVSP', period='1d', interval='5m')
    if indice == 'S&P500':
        indice_diario = yf.download('^GSPC', period='1d', interval='5m')
    if indice == 'NASDAQ':
        indice_diario = yf.download('^IXIC', period='1d', interval='5m')

    fig = go.Figure(data=[go.Candlestick(x=indice_diario.index,
                        open=indice_diario['Open'],
                        high=indice_diario['High'],
                        low=indice_diario['Low'],
                        close=indice_diario['Close'])])
    fig.update_layout(title=indice, xaxis_rangeslider_visible=False)

    st.plotly_chart(fig)


    st.markdown('---')

    lista_acoes = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'CSNA3.SA']

    acao = st.selectbox('Selecione a Ação', lista_acoes)

    hist_acao = yf.download(acao, period='1d', interval='5m')

    fig_acao = go.Figure(data=[go.Candlestick(x=hist_acao.index,
                                         open=hist_acao['Open'],
                                         high=hist_acao['High'],
                                         low=hist_acao['Low'],
                                         close=hist_acao['Close'])])
    fig_acao.update_layout(title=acao, xaxis_rangeslider_visible=False)

    st.plotly_chart(fig_acao)









def mapa_mensal():
    st.title('Análise de Retornos Mensais')

    with st.expander('Escolha', expanded=True):
        opcao = st.radio('Selecione', ['Índices', 'Ações'])

    if opcao =='Índices':
        with st.form(key='form_indice'):
            ticker = st.selectbox('Índice', ['^BVSP', 'IFNC', 'IMAT'])
            analisar = st.form_submit_button('Analisar')

    else:
        with st.form(key='form_acoes'):
            ticker = st.selectbox('Ações', ['PETR4.SA', 'VALE3', 'ITUB4'])
            analisar = st.form_submit_button('Analisar')

    retornos =  yf.download(ticker, period='5y')['Close']
    r1 = ''
    if analisar:
        dt_ini = '01/12/1999'
        dt_fim = '31/12/2023'

        if opcao == 'Índices':
            retornos =  yf.download(ticker, period='5y')['Close']
          #  r1 = float(retornos[1].split(' ')[-1])
        else:
            retornos = yf.download(ticker, period='5y')['Close']
    st.write(retornos)

    # seprar e agrupar os anos e meses
    retorno_mensal = retornos.groupby([retornos.index.year.rename('Year'), retornos.index.month.rename('Month')])
    st.write(retorno_mensal.agg)


def fundamentos():
    st.title('Informações sobre Fundamentos')

    lista_tickers = fd.list_papel_all()

    comparar = st.checkbox('Comparar dois ativos')

    col1, col2 = st.columns(2)

    with col1:
        with st.expander('Ativo 1', expanded=True):
            papel1 = st.selectbox('Selecione o Papel', lista_tickers)
            info_papel1 = fd.get_detalhes_papel(papel1)
            st.write('**Empresa:**', info_papel1['Empresa'][0])
            st.write('**Setor:**', info_papel1['Setor'][0])
            st.write('**Subsetor:**', info_papel1['Subsetor'][0])
            st.write('**Valor de Mercado:**', f"R$ {info_papel1['Valor_de_mercado'][0]:,.2f}")
            st.write('**Patrimônio Líquido:**', f"R$ {float(info_papel1['Patrim_Liq'][0]):,.2f}")
            st.write('**Receita Liq. 12m:**', f"R$ {float(info_papel1['Receita_Liquida_12m'][0]):,.2f}")
            st.write('**Dívida Bruta:**', f"R$ {float(info_papel1['Div_Bruta'][0]):,.2f}")
            st.write('**Dívida Líquida:**', f"R$ {float(info_papel1['Div_Liquida'][0]):,.2f}")
            st.write('**P/L:**', f"R$ {float(info_papel1['PL'][0]):,.2f}")
            st.write('**Dividend Yield:**', f"{info_papel1['Div_Yield'][0]}")

    if comparar:
        with col2:
            with st.expander('Ativo 2', expanded=True):
                papel2 = st.selectbox('Selecione o 2º Papel', lista_tickers)
                info_papel2 = fd.get_detalhes_papel(papel2)
                st.write('**Empresa:**', info_papel2['Empresa'][0])
                st.write('**Setor:**', info_papel2['Setor'][0])
                st.write('**Subsetor:**', info_papel2['Subsetor'][0])
                st.write('**Valor de Mercado:**', f"R$ {info_papel2['Valor_de_mercado'][0]:,.2f}")
                st.write('**Patrimônio Líquido:**', f"R$ {float(info_papel2['Patrim_Liq'][0]):,.2f}")
                st.write('**Receita Liq. 12m:**', f"R$ {float(info_papel2['Receita_Liquida_12m'][0]):,.2f}")
                st.write('**Dívida Bruta:**', f"R$ {float(info_papel2['Div_Bruta'][0]):,.2f}")
                st.write('**Dívida Líquida:**', f"R$ {float(info_papel2['Div_Liquida'][0]):,.2f}")
                st.write('**P/L:**', f"R$ {float(info_papel2['PL'][0]):,.2f}")
                st.write('**Dividend Yield:**', f"{info_papel2['Div_Yield'][0]}")







def main():
    st.sidebar.image('masqueico.jpeg', width=200)
    st.sidebar.title('App Financeiro')
    st.sidebar.markdown('---')
    lista_menu=['Home', 'Panorama do Mercado', 'Rentabilidades Mensais', 'Fundamentos']
    escolha= st.sidebar.radio('Escolha a opção', lista_menu)

    if escolha == 'Home':
        home()
    if escolha == 'Panorama do Mercado':
        panorama()
    if escolha == 'Rentabilidades Mensais':
        mapa_mensal()
    if escolha == 'Fundamentos':
        fundamentos()



main()

