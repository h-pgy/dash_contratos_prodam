import streamlit as st
import pandas as pd
import plotly.express as px
from utils.serialize_df import read_parquet_df


#carregamento dos dados
file_dados = 'dados_contratos_prodam_limpos.parquet'
df: pd.DataFrame = read_parquet_df(file_dados)

with st.sidebar:
    st.header("Sobre")

    st.markdown('Dashboard desenvolvido por Henrique Pougy - SEPLAN/CODATA')

    with st.expander("Fonte dos dados"):
        st.markdown(
            """
            Os dados apresentados neste dashboard foram extraídos da [API do Sistema de Orçamento e Finanças (SOF)](https://capital.sp.gov.br/web/fazenda/contaspublicas/apisof) da Prefeitura de São Paulo.
            
            O recorte inclui **todos os contratos da empresa Prodam** assinados no ano de **2024**, com dados de execução contratual atualizados.
            
            As informações foram processadas previamente para fins de visualização e análise agregada.
            """
        )



st.markdown(
    """
    <div style="
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Pal%C3%A1cio_do_Anhangaba%C3%BA_%28Ed._Matarazzo%29_01.JPG/800px-Pal%C3%A1cio_do_Anhangaba%C3%BA_%28Ed._Matarazzo%29_01.JPG');
        background-size: cover;
        background-position: center;
        filter: grayscale(100%);
        opacity: 0.8;
        height: 200px;
        width: 100%;
        position: relative;
        border-radius: 10px;
    ">
    </div>

    <div style="
        margin-top: -160px;
        text-align: center;
        color: black;
        position: relative;
        z-index: 1;
    ">
        <h1 style="margin-bottom: 0;">Dashboard - Contratos da Prodam</h1>
        <h3 style="margin-top: 5px;">com o Município de São Paulo</h3>
    </div>
    """,
    unsafe_allow_html=True
)



st.header("Dados gerais para todos os contratos da Prodam")

quantidade_de_contratos = len(df)
valor_total_pago = df['valPago'].sum() / 1_000_000
media_valor_por_contrato = (df['valPago'].sum()/quantidade_de_contratos) / 1_000_000

col1, col2, col3 = st.columns(3)

col1.metric("Quantidade de contratos", f"{quantidade_de_contratos}")
col2.metric("Valor total pago", f"R$ {valor_total_pago:,.2f} mi")
col3.metric("Valor pago médio por contrato", f"R$ {media_valor_por_contrato:,.2f} mi")

#grafico de dispersaoo da execucao contratual


df_plot = df.groupby('txtDescricaoOrgao').sum().reset_index()

df_plot['percentual_executado'] = df_plot['valPago']/df_plot['valEmpenhadoLiquido']
df_plot = df_plot[df_plot['percentual_executado'].notnull()]

fig = px.scatter(
    df_plot,
    x="valEmpenhadoLiquido",
    y="percentual_executado",
    size="valPago",
    hover_name="txtDescricaoOrgao",
    labels={
        "valEmpenhadoLiquido": "Valor Empenhado Líquido Total (R$)",
        "valPago": "Valor Pago Total (R$)",
        "percentual_executado": "Percentual Executado"
    },
    title="Dispersão das Secretarias por Execução Contratual",
)

fig.update_layout(
    xaxis_title="Valor Empenhado Líquido (R$)",
    yaxis_title="Execução contratual (%)",
    legend_title="",
    hovermode="closest"
)

st.plotly_chart(fig, use_container_width=True)

# Criar histograma interativo dos valores pagos

valores_pagos = df.groupby('txtDescricaoOrgao')['valPago'].sum().dropna()
valores_pagos = valores_pagos.astype(float)


fig = px.histogram(
    valores_pagos,
    x=valores_pagos,
    nbins=30,
    histnorm="probability density",
    opacity=0.6
)

fig.update_traces(marker_line_width=1, marker_line_color="black")
fig.update_layout(
    xaxis_title="Valor pago (R$)",
    yaxis_title="Densidade estimada",
    title="Distribuição dos valores pagos por contrato (densidade estimada)"
)

st.plotly_chart(fig, use_container_width=True)

st.header("Acompanhamento da execução contratual por órgão")


# Filtros interativos
orgaos = df["txtDescricaoOrgao"].dropna().unique()
orgao_selecionado = st.selectbox("Selecione o órgão", sorted(orgaos))

df_filtrado = df[df["txtDescricaoOrgao"] == orgao_selecionado]


#indicadores principais

st.subheader("Valores de contratação")
qtd_contratos = df_filtrado["codContrato"].nunique()
valor_total_pago = df_filtrado["valPago"].sum()
media_valor_por_contrato = valor_total_pago / qtd_contratos if qtd_contratos else 0


col1, col2, col3 = st.columns(3)

col1.metric("Quantidade de contratos", f"{qtd_contratos}")
col2.metric("Valor total pago", f"R$ {valor_total_pago:,.2f}")
col3.metric("Valor pago médio por contrato", f"R$ {media_valor_por_contrato:,.2f}")

# Métricas de Execução Contratual
st.subheader("Execução Contratual")

percentual_anulado = df['valAnuladoEmpenho'].sum()/df['valTotalEmpenhado'].sum()
percentual_aditado = df['valAditamentos'].sum()/df['valEmpenhadoLiquido'].sum()
percentual_reajustado = df['valReajustes'].sum()/df['valEmpenhadoLiquido'].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Percentual anulado", f"{percentual_anulado:,.2%}")
col2.metric("Percentual aditado", f"{percentual_aditado:,.2%}")
col3.metric("Percentual reajustado", f"{percentual_reajustado:,.2%}")

st.subheader("Detalhes da execução contratual")
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Empenhado", f"R$ {df_filtrado['valTotalEmpenhado'].sum():,.2f}")
    st.metric("Total Anulado", f"R$ {df_filtrado['valAnuladoEmpenho'].sum():,.2f}")


with col2:
    st.metric("Total de Aditamentos", f"R$ {df_filtrado['valAditamentos'].sum():,.2f}")
    st.metric("Total Reajustes", f"R$ {df_filtrado['valReajustes'].sum():,.2f}")



# Tabela com os contratos filtrados
st.subheader("Detalhes dos Contratos")
st.dataframe(df_filtrado[[
    'codProcesso', 'codContrato', 'txtDescricaoModalidade', 'txtTipoContratacao', 'txtObjetoContrato', 'datAssinaturaContrato', 'datVigencia',
    'valTotalEmpenhado', 'valEmpenhadoLiquido', 'valAditamentos', 'valReajustes', 'valPago'
]])