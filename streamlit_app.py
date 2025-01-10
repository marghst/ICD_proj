# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="Dashboard - Usos de Data Science e Big Data no Planeamento Urbano",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

#######################
# CSS styling
st.markdown("""
<style>
/* Rodapé fixo */
footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #f1f1f1;
    text-align: center;
    padding: 10px 0;
    font-size: 14px;
    font-family: Arial, sans-serif;
    color: #333333;
    z-index: 9999;
}

/* Ajuste no container principal */
[data-testid="block-container"] {
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Estilo das abas */
.streamlit-tab {
    font-size: 18px;
    font-weight: bold;
    padding: 10px;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

#######################
# Query fixa
query = """ Query: Data Science OR Big Data AND (Urban Planning OR Urban Management OR Spatial Planning OR Urban Development), 
limited to Social Sciences"""

#######################
# Load data (Exemplo)
df_all = pd.read_csv(r'C:\Users\Margarida\OneDrive - Universidade de Coimbra\Mestrado CDSC_1\1º ano\Introdução à Ciência de Dados\proj_ICD2\dados_streamlit\df_all_geral.csv')

# Criar a coluna 'count' com o número de artigos por país e ano
df_all['count'] = 1  # Inicializar com 1 para representar cada artigo
df_all = df_all.groupby(['year', 'affiliation-country'], as_index=False).agg({'count': 'sum'})

#######################
# Tabs
tab1, tab2 = st.tabs(["📚 Análise Bibliográfica", "📈 Análise Bibliométrica"])

#######################
# Tab 1: Análise Bibliográfica
with tab1:
    st.title("📚 Análise Bibliográfica")
    st.write("Nesta aba, apresentamos a análise detalhada dos artigos com base na query fornecida.")

    # Mapa por ano ou total
    st.sidebar.title("Configurações de Filtro")
    year_list = sorted(df_all.year.unique(), reverse=True)
    selected_year = st.sidebar.selectbox('Selecione o Ano', ["Total"] + year_list)
    selected_color_theme = st.sidebar.selectbox('Escolha o Tema de Cores', ['Viridis', 'Inferno', 'Cividis', 'Blues', 'Turbo', 'Rainbow'])

    # Filtrar os dados com base no ano selecionado
    if selected_year == "Total":
        df_filtered = df_all.groupby("affiliation-country", as_index=False).agg({"count": "sum"})
    else:
        df_filtered = df_all[df_all["year"] == selected_year]

    # Renomear colunas para uso no mapa
    df_filtered.rename(columns={"affiliation-country": "País", "count": "Número de Artigos"}, inplace=True)

    # Criar o mapa
    def make_map(input_df, color_theme):
        fig = px.choropleth(
            input_df,
            locations="País",
            locationmode="country names",
            color="Número de Artigos",
            hover_name="País",
            color_continuous_scale=color_theme,
            title=f"Número de Artigos por País ({selected_year})"
        )

        fig.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
            coloraxis_colorbar=dict(title="Número de Artigos"),
        )
        return fig

    # Exibir o mapa
    st.plotly_chart(make_map(df_filtered, selected_color_theme), use_container_width=True)

#######################
# Tab 2: Análise Bibliométrica
with tab2:
    st.title("📈 Análise Bibliométrica")
    st.write("Nesta aba, apresentamos métricas e análises bibliométricas com base nos artigos selecionados.")

    # Adicione aqui outras visualizações ou análises
    st.write("Esta seção está em desenvolvimento. Inclua gráficos, tabelas ou outras visualizações relevantes aqui.")

#######################
# Rodapé fixo
st.markdown(f"""
<footer>
    Query utilizada: <b>{query}</b>
</footer>
""", unsafe_allow_html=True)
