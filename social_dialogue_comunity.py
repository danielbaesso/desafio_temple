import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import dash_leaflet as dl

# Criar app Dash
app = dash.Dash(__name__)

# Exemplo de dados fictícios com novas colunas e mais comunidades
data = {
    "Comunidade": [
        "Quilombola A", "Quilombola B", "Indígena X", "Indígena Y", "Rural Z", 
        "Quilombola C", "Rural A", "Indígena Z", "Quilombola D", "Indígena W",
        "Rural B", "Rural C", "Indígena V", "Quilombola E", "Rural D"
    ],
    "Impacto": [
        "Alto", "Médio", "Alto", "Baixo", "Médio", 
        "Médio", "Alto", "Baixo", "Alto", "Médio", 
        "Baixo", "Médio", "Alto", "Baixo", "Médio"
    ],
    "Resistência": [80, 60, 90, 40, 50, 65, 85, 30, 75, 55, 50, 65, 90, 45, 60],
    "IDH": [0.7, 0.6, 0.8, 0.5, 0.6, 0.65, 0.72, 0.55, 0.78, 0.69, 0.60, 0.62, 0.74, 0.58, 0.63],
    "Salário Médio": [1200, 1500, 1000, 1100, 1300, 1250, 1400, 950, 1350, 1150, 1100, 1250, 1450, 1050, 1200],
    "Acesso à Educação": [85, 70, 95, 60, 75, 80, 90, 55, 88, 65, 72, 85, 92, 60, 78],
    "Latitude": [
        -7.0, -7.1, -7.2, -7.3, -7.4, 
        -6.5, -7.5, -6.8, -6.7, -7.2, 
        -7.3, -6.6, -7.1, -6.9, -7.0
    ], 
    "Longitude": [
        -42.0, -42.1, -42.2, -42.3, -42.4, 
        -42.5, -42.8, -42.6, -42.9, -43.0, 
        -42.7, -42.3, -42.1, -42.2, -42.5
    ]
}

df = pd.DataFrame(data)

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard de Impacto das PCHs", style={'textAlign': 'center', 'color': '#333'}),

    # Seção de gráficos e mapa
    html.Div([
        html.Div([
            html.H3("Selecione o Impacto", style={'textAlign': 'center', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='impacto',
                options=[
                    {'label': 'Todos', 'value': 'Todos'}
                ] + [{'label': i, 'value': i} for i in df["Impacto"].unique()],
                value='Todos',
                clearable=False,
                style={'width': '100%', 'padding': '10px'}
            ),
            dcc.Graph(id='grafico_resistencia', style={'height': '300px'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            dl.Map([dl.TileLayer(), dl.LayerGroup(id="mapa_comunidades")], center=[-7.2, -42.2], zoom=8, style={'height': '400px', 'width': '100%'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
    ], style={'display': 'flex', 'justify-content': 'space-between', 'padding': '10px'}),

    # Tabela de dados
    html.Div([
        dash_table.DataTable(
            id='tabela_dados',
            columns=[{"name": col, "id": col} for col in df.columns if col not in ['Latitude', 'Longitude']],  # Removido Latitude e Longitude
            data=df.to_dict('records'),
            style_table={'width': '100%', 'overflowX': 'auto', 'border': '1px solid #ddd'},
            style_cell={'textAlign': 'left', 'padding': '10px', 'fontSize': '14px'},
            style_header={'backgroundColor': '#f0f0f0', 'fontWeight': 'bold', 'textAlign': 'center'},
            style_data={'backgroundColor': '#fafafa'},
            row_selectable='multi',
            selected_rows=[]
        )
    ], style={'padding': '20px'})
])

# Callback para atualizar gráfico, mapa e tabela ao selecionar na tabela e no Dropdown
@app.callback(
    [Output('grafico_resistencia', 'figure'),
     Output('mapa_comunidades', 'children')],
    [Input('tabela_dados', 'selected_rows'),
     Input('impacto', 'value')]
)
def update_dashboard(selected_rows, impacto_filtro):
    # Filtra os dados com base no filtro do Dropdown
    if impacto_filtro != 'Todos':
        dff = df[df['Impacto'] == impacto_filtro]
    else:
        dff = df
    
    if selected_rows:
        dff = dff.iloc[selected_rows]

    # Gráfico com uma cor mais visível
    fig = px.bar(dff, x='Comunidade', y='Resistência', title="Resistência Comunitária",
                 color='Impacto', color_discrete_map={"Alto": "red", "Médio": "orange", "Baixo": "green"})

    # Criar marcadores no mapa
    mapa_markers = [dl.Marker(position=[row["Latitude"], row["Longitude"]],
                               children=dl.Tooltip(row["Comunidade"])) for _, row in dff.iterrows()]

    return fig, mapa_markers

# Rodar o app
if __name__ == '__main__':
    app.run(debug=True)
