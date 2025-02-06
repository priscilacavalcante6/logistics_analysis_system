import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações do Dashboard
# st.set_page_config(page_title="Dashboard de Análise Logítica", page_icon="icons8-analytics-48.png", layout="wide")


# Função para exibir o painel
def painel():
    st.title("Painel Logística")
    st.write("Bem-vindo ao painel de logística!")

    # Adicione aqui o conteúdo do painel de logística

# Chamando a função de painel se o usuário estiver logado
if "usuario" in st.session_state and st.session_state["usuario"]:
    painel()
else:
    st.error("Você precisa fazer login primeiro!")


# Carregar os dados
file_path = "dados_logisticos.csv"
try:
    df = pd.read_csv(file_path)
    # Verificar se as colunas necessárias existem
    required_columns = ["Data Pedido", "Data Entrega", "Prioridade", "Estoque Atual", "Estoque Mínimo", "Tipo Mercadoria", "Lat Retirada", "Lon Retirada"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Colunas necessárias não encontradas no arquivo: {', '.join(missing_columns)}")
        st.stop()
except pd.errors.EmptyDataError:
    st.error(f"Arquivo {file_path} está vazio.")
    st.stop()
except Exception as e:
    st.error(f"Erro ao ler o arquivo {file_path}: {e}")
    st.stop()

st.markdown(
    """
    <style>
        /* Fundo geral em cinza mais claro */
        body, .stApp {
            background: linear-gradient(to bottom, #F5F5F5, #E8E8E8, #DCDCDC);
            color: black;
        }
        
        /* Barra lateral */
        [data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #E0E0E0, #A9A9A9);
        }

        /* Cabeçalho - Cinza escuro sólido */
        header, [data-testid="stHeader"] {
            background-color: #3A3A3A !important;
            color: white;  /* Mantém o texto branco para contraste */
            padding: 10px;
            text-align: center;
        }


        /* Rodapé */
        footer {
            background: linear-gradient(to top, #A9A9A9, #808080);
            color: black;
            padding: 10px;
            text-align: center;
        }

        /* Remove fundo branco dos gráficos */
        .stPlotlyChart, .stImage {
            background-color: transparent !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# Converter colunas de data
df["Data Pedido"] = pd.to_datetime(df["Data Pedido"])
df["Data Entrega"] = pd.to_datetime(df["Data Entrega"])

# Criar coluna de atraso
df["Atraso"] = (df["Data Entrega"] > df["Data Pedido"] + pd.to_timedelta(3, unit="D"))

# Criar Status de Entrega
df["Status da Entrega"] = df.apply(lambda row: "Atrasado" if row["Atraso"] else "No Prazo", axis=1)


# 📂 MENU LATERAL
# Exibir imagem na barra lateral
st.sidebar.image("logo1.png", width=200)
st.sidebar.markdown(
    """
    <h2 style='font-size: 10px;'>Seu logotipo aqui</h2>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown(
    """
    <h1 style='color: grey; font-weight: bold;'>Filtros</h1>
    """,
    unsafe_allow_html=True
)

# Filtro por Prioridade
prioridade = st.sidebar.multiselect("Prioridade", df["Prioridade"].unique(), default=df["Prioridade"].unique())

# Filtro por Status da Entrega
status = st.sidebar.radio("Status da Entrega", ["Todos", "No Prazo", "Atrasado"])

# 🔍 Aplicar Filtros
df_filtrado = df[df["Prioridade"].isin(prioridade)]
if status != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Status da Entrega"].str.lower() == status.lower()]

# 🔹 KPIs principais
st.title("📦 Painel de Análise Logística")

# Linha Divisória
st.markdown("<hr style='border: 3px solid #00FF00; margin: 20px 0;'>",
            unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("🚛 Pedidos Totais", len(df_filtrado), delta_color="inverse")
col2.metric("⏳ Pedidos Atrasados", df_filtrado["Atraso"].sum(), delta_color="inverse")
col3.metric("📉 Estoque Baixo", (df_filtrado["Estoque Atual"] < df_filtrado["Estoque Mínimo"]).sum(), delta_color="inverse")

# Adicionando estilo para letras em branco e negrito
st.markdown(
    """
    <style>
    .stMetric label {
        color: Grey;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Linha Divisória
st.markdown("<hr style='border: 3px solid #00FF00; margin: 20px 0;'>",
            unsafe_allow_html=True)


# Adicionando o título da página
st.markdown("<h1 style='font-size: 26px; text-align: left;'>📊 Análise de Entregas</h1>", unsafe_allow_html=True)

# Criando o seletor de abas
aba_selecionada = st.radio("Escolha a seção", ["Eficiência das Entregas", "Tabela de Dados"])

if aba_selecionada == "Eficiência das Entregas":
    # Mostrar gráfico apenas na página correta
    # st.subheader(" Eficiência das Entregas por Tipo de Mercadoria")
    # Configurar o tema e o tamanho da fonte
    # st.markdown(
    #     """
    #     <style>
    #     .reportview-container .main .block-container {
    #         font-size: 5px;
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )
    eficiencia_por_tipo = df_filtrado.groupby("Tipo Mercadoria")["Atraso"].mean().reset_index()
    eficiencia_por_tipo["Eficiência"] = 1 - eficiencia_por_tipo["Atraso"]
    fig_eficiencia = px.bar(eficiencia_por_tipo, 
                        x="Tipo Mercadoria", 
                        y="Eficiência", 
                        # title="Eficiência das Entregas por Tipo de Mercadoria",
                        labels={"Eficiência": "Eficiência (%)"},
                        color="Eficiência",
                        color_continuous_scale=px.colors.sequential.Viridis)
    fig_eficiencia.update_layout(yaxis_tickformat=".0%")
    fig_eficiencia.update_traces(
        texttemplate='<b>%{y:.0%}</b>',  # Formato do rótulo em porcentagem
        textposition='outside' )       # Posição do rótulo

    # Ajustes nos rótulos
    fig_eficiencia.update_traces(textfont_size=9, 
                    textfont_family="Arial", 
                    textfont_color="black",
                    textposition="inside",  # Coloca o texto dentro da barra
                    insidetextanchor="middle")  # Centraliza o texto

    # Ajuste do layout
    fig_eficiencia.update_layout(
        uniformtext_minsize=12,  
        uniformtext_mode='hide',
        margin=dict(t=50, b=100),
        xaxis_title="Tipo de Mercadoria",
        yaxis_title="Eficiência",
        legend_title="Status da Entrega",
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",  # Remove o fundo geral
        plot_bgcolor="rgba(0,0,0,0)"    # Remove o fundo do gráfico   
    )

    # Exibe o gráfico na página correta
    st.plotly_chart(fig_eficiencia, use_container_width=True)
else:
    st.subheader("📋 Tabela de Dados Logísticos")
    colunas_disponiveis = df_filtrado.columns.tolist()
    colunas_selecionadas = st.multiselect("Selecione as colunas que deseja visualizar:", colunas_disponiveis, default=colunas_disponiveis)
    df_tabela = df_filtrado[colunas_selecionadas]
    st.dataframe(df_tabela)

# Linha Divisória
st.markdown("<hr style='border: 3px solid #00FF00; margin: 20px 0;'>",
            unsafe_allow_html=True)

# Criando o gráfico de pizza
st.subheader("📊 Status das Entregas")
fig_status = px.pie(df_filtrado, names="Status da Entrega", title="Distribuição de Status")

# Ajustando o tamanho da pizza e os rótulos
fig_status.update_traces(
    textinfo='percent+label',  # Exibe a porcentagem e o rótulo
    textfont=dict(size=12, family="Arial", color="black", weight='bold'),  # Fonte em negrito e maior
    marker=dict(
        colors=px.colors.sequential.Viridis_r  # Usando a escala de cores Viridis
    )
)

# Ajuste no layout para remover fundo e melhorar espaçamento
fig_status.update_layout(
    autosize=False,
    margin=dict(t=30, b=30, l=30, r=30),  # Ajusta o espaçamento das bordas
    font=dict(size=12, family="Arial", color="grey"),
    paper_bgcolor="rgba(0,0,0,0)",  # Remove o fundo geral
    plot_bgcolor="rgba(0,0,0,0)"    # Remove o fundo do gráfico
)

# Exibe o gráfico
st.plotly_chart(fig_status, use_container_width=True)

# Linha Divisória
st.markdown("<hr style='border: 3px solid #00FF00; margin: 20px 0;'>",
            unsafe_allow_html=True)

df_filtrado['Data Pedido'] = pd.to_datetime(df_filtrado['Data Pedido'])
df_filtrado['Data Entrega'] = pd.to_datetime(df_filtrado['Data Entrega'])

# Calculando o tempo de entrega em dias
df_filtrado["Tempo Entrega"] = (df_filtrado["Data Entrega"] - df_filtrado["Data Pedido"]).dt.days

# Criando um status de entrega
df_filtrado["Status Entrega"] = df_filtrado["Tempo Entrega"].apply(lambda x: "Atrasado" if x > 3 else "No Prazo")

# Definição de cores
cores = {"Atrasado": "red", "No Prazo": "green"}

# Criando o gráfico
st.subheader("📍 Locais para Retirada")
fig_tempo = px.histogram(df_filtrado, x="Tempo Entrega", color="Status Entrega", 
                        # nbins=2, title="Distribuição de Tempo de Entrega",
                        color_discrete_map=cores, text_auto=True)  # Adiciona rótulos de contagem

# Ajustando o título do gráfico
fig_tempo.update_layout(
    title={
        'text': "Distribuição de Tempo de Entrega",
        'y': 1.0,  # Aproxima o título do gráfico
        'x': 0.0,  # Alinha o título à esquerda
        'xanchor': 'left',
        'yanchor': 'top',
        'font': dict(size=12, color='grey', family="Arial", weight='bold'),
    }
)

# Ajuste do layout do gráfico
fig_tempo.update_layout(
    xaxis_title="Tempo de Entrega (dias)",
    yaxis_title="Frequência (Entregas)",
    xaxis=dict(tickmode="linear", tick0=0, dtick=1, tickangle=45),
    font=dict(size=10, family="Arial", color="grey",weight="bold"),
    title_font=dict(size=10, family="Arial", color="black", weight="bold"),
    paper_bgcolor="rgba(0,0,0,0)",  # Remove o fundo geral
    plot_bgcolor="rgba(0,0,0,0)",   # Remove o fundo do gráfico 
    bargap=0.2
)

# Ajustando as barras e rótulos
fig_tempo.update_traces(
    marker=dict(opacity=0.7, line=dict(width=0)),  # Remove bordas das barras
    textfont_size=10, textfont_family="Arial", textfont_color="black",textfont_weight="bold",  # Ajusta fonte dos rótulos
    texttemplate='%{y:.0f}'  # Exibe apenas valores inteiros  
)
if "Lat Retirada" in df_filtrado.columns and "Lon Retirada" in df_filtrado.columns:
    # st.markdown("<h3 style='font-size: 10px;'>📍 Locais de Retirada</h3>", unsafe_allow_html=True)

    # Definir a cor com uma escala contínua baseada no estoque
    fig_mapa = px.scatter_mapbox(
        df_filtrado, lat="Lat Retirada", lon="Lon Retirada", 
        color="Estoque Atual",  # Usando o estoque atual para colorir os pontos
        color_continuous_scale="Viridis",  # Melhor paleta de cores para percepção visual
        size="Estoque Atual",  # O tamanho das bolhas varia conforme o estoque
        size_max=30,  # Limite máximo de tamanho para as bolhas
        zoom=5, 
        mapbox_style="carto-positron",  # Estilo de mapa mais limpo
        # title="📍 Mapa de Locais de Retirada",
        hover_name="Estoque Atual", 
        hover_data={
            "Lat Retirada": False, 
            "Lon Retirada": False, 
            "Estoque Atual": True,  # Exibe a quantidade de estoque ao passar o mouse
        },
    )

    # Ajustando a aparência do mapa
    fig_mapa.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),  # Ajusta as margens para aproveitar melhor o espaço
        height=500,  # Ajusta o tamanho do mapa
        showlegend=True,  # Exibe a legenda de forma informativa
        legend_title="Estoque Atual",  # Título da legenda
    )

    # Centralizar o mapa com base no centro das coordenadas
    fig_mapa.update_layout(mapbox_center={"lat": df_filtrado["Lat Retirada"].mean(), 
                                        "lon": df_filtrado["Lon Retirada"].mean()})

    # Exibir o mapa no Streamlit
    st.plotly_chart(fig_mapa, use_container_width=True)

# Linha Divisória Estilizada  
st.markdown(
    "<hr style='border: 3px solid #00FF00; margin: 20px 0;'>", unsafe_allow_html=True
)

# 📋 Tabela de Dados Filtrada
import streamlit as st
import pandas as pd

# Carregar os dados (substituir pelo seu arquivo CSV)
file_path = "dados_logisticos.csv"


# Exibir todas as colunas disponíveis para seleção
# st.subheader("📋 Tabela de Dados Logísticos")

# # Criar um filtro interativo para escolher colunas
# colunas_disponiveis = df.columns.tolist()
# colunas_selecionadas = st.multiselect("Selecione as colunas que deseja visualizar:", colunas_disponiveis, default=colunas_disponiveis)

# # Filtrar o DataFrame com as colunas escolhidas
# df_filtrado = df[colunas_selecionadas]

# # Exibir a tabela filtrada
# st.dataframe(df_filtrado)

