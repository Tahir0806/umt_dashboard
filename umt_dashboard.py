import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc,Input,Output
import dash_bootstrap_components as dbc

df = pd.read_excel("umt_stats01.xlsx")

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server=app.server

bar_chart=px.bar(
    df,
    x=df["Year"],
    y=df["Total_Admissions"],
    color="Year",
    title="Admissions Over Years",
    template="plotly_dark"
)
bar_chart.update_layout(paper_bgcolor="rgba(0,0,0,0)", 
                        plot_bgcolor="rgba(0,0,0,0)",
                        xaxis_title="Year", 
                        yaxis_title="Total Admissions",
                        width=650,  height=200, autosize=True, 
                        margin=dict(l=70, r=20, t=50, b=0))
line_chart = px.line(
    df,
    x="Year",
    y=df.columns[2],
    markers=True,
    title="Performance Trend",
    template="plotly_dark"
)
line_chart.update_traces(line=dict(color="#FF851B", width=2))
line_chart.update_layout(paper_bgcolor="rgba(0,0,0,0)", 
                         plot_bgcolor="rgba(0,0,0,0)",
                         xaxis_title="Year", 
                         yaxis_title="Graduates",
                         width=650, height=200, autosize=True, 
                         margin=dict(l=70, r=20, t=50, b=0),
                         xaxis=dict(showgrid=True, gridcolor="grey"),
                         yaxis=dict(showgrid=True, gridcolor="grey")),
pie_chart = px.pie(
    df,
    names="Year",
    values="Graduate_rate",
    title="Graduates Rate since 2020",
    template="plotly_dark",
    hole=0.5,
    category_orders={"Year": sorted(df["Year"].unique())}
)
pie_chart.update_traces(
    textinfo="value",texttemplate="%{value:.2f}%",
    textfont_color="white",
    pull=[0.04, 0.04, 0.04, 0.04, 0.04]
)
pie_chart.update_layout(paper_bgcolor="rgba(0,0,0,0)", 
                        plot_bgcolor="rgba(0,0,0,0)",
                        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5,font=dict(color="white")),
                        margin=dict(l=10, r=10, t=80, b=20))

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(
                    src="/assets/myphoto_02.jpg", 
                    style={
                        "width": "40px",
                        "height": "40px",
                        "borderRadius": "50%",
                        "marginRight": "15px",
                        "marginTop": "5px",
                        "marginLeft": "10px"
                    }),
                html.Span(
                    "Tahir M.",
                    style={
                        "fontSize": "18px",
                        "fontWeight": "bold",
                        "color": "white",
                        "verticalAlign": "middle"
                    }),
            ],style={"display": "flex","alignItems": "center"})
        ], width="auto"),
        dbc.Col([
            html.H1("📊 UMT DashBoard", 
            className="text-center text-white mt-2",
            style={"fontSize":"22px","fontWeight":"bold","marginLeft":"-150px"})
        ])
    ], justify="start", className="mt-2 mb-3"),
    html.Hr(style={"borderTop": "2px solid white"}),
    dbc.Row([
        dbc.Col([
            html.H5("Select Year",className="text-white",
                    style={"fontSize":"17px","marginBottom":"5px"}),
            dcc.Dropdown(id="year_dropdown",
                         value=df["Year"].iloc[0], 
                        options=[{"label": str(y), "value": y} for y in df["Year"]],
                        style={"width":"220px","marginBottom":"8px",
                        "backgroundColor": "#DFE1E3", "color": "black",
                        "borderRadius": "6px","boxShadow": "inset 0 2px 10px rgba(0,0,0,0.3),inset 0 -2px 10px rgba(0,0,0,0.3)"}),
            dbc.Card(
                dbc.CardBody([
                    html.H6("Key Metrics", 
                            className="text-center mb-2",
                            style={"fontSize":"20px","fontWeight":"bold",
                                   "color":"orange"}),
                    html.Hr(),
                    html.Div(
                        id="scholarships_bubble",
                        className="text-white mt-4 mb-4"
                        ),
                    html.Hr(),
                    html.Div(
                        id="revenue",
                        className="text-white mt-4 mb-4"
                        ),
                    html.Hr(),
                    html.Div(
                        id="research_papers",
                        className="text-white mt-4 mb-4"
                        )
        ]),style={"background":"linear-gradient(100deg, #08335e,#325f8a)","borderRadius": "10px",
                  "height":"392px","width":"220px","boxShadow": "inset 0 2px 10px rgba(0,0,0,0.3),inset 0 -2px 10px rgba(0,0,0,0.3)"
                  })
        ]),
        dbc.Col([
            dbc.Card(
                dbc.CardBody(dcc.Graph(figure=line_chart),
                            style={"padding":"0"}),
                className="mt-4",
                style={"background":"linear-gradient(100deg, #08335e,#325f8a)","borderRadius": "10px",
                       "width": "650px","height":"216px","marginBottom": "8px",
                       "marginLeft": "-280px"}
            ),
            dbc.Card(
                dbc.CardBody(dcc.Graph(figure=bar_chart),
                             style={"padding":"0"}),
                style={"background":"linear-gradient(100deg,#325f8a,#08335e)","borderRadius": "10px",
                       "width": "650px","height":"216px","marginLeft": "-280px"}
            )], width="auto"),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(dcc.Graph(figure=pie_chart),
                             style={"padding":"1px"}),
                className="mt-4",
                style={"background":"linear-gradient(100deg, #08335e,#325f8a)", "borderRadius": "10px",
                       "width": "350px","height": "440px","marginLeft": "-18px"}
            ), width="auto")
    ],className="d-flex justify-content-end")
    
], fluid=True, style={"backgroundColor": "#1A2633", "minHeight": "100vh", "padding": "20px"})

@app.callback(
    Output("scholarships_bubble", "children"),
    Input("year_dropdown", "value")
)
def update_scholarships_bubble(selected_year):
    filtered_df = df[df["Year"] == selected_year]
    total_scholarships = filtered_df["Scholarships_Awarded"].sum()
    return [
        html.Span("• ", style={"fontSize": "20px", "marginRight": "8px","verticalAlign": "middle"}),
        html.Span(f"{total_scholarships:,}",style={"fontSize": "24px","fontWeight":"bold","color": "#00ffcc"}),
        html.Span("Scholarships Awarded", style={"fontSize": "16px","marginLeft":"5px"})
    ]

@app.callback(
    Output("revenue", "children"),
    Input("year_dropdown", "value")
)
def update_revenue(selected_year):
    filtered_df = df[df["Year"] == selected_year]
    total_revenue = filtered_df["Revenue_Million_PKR"].sum()
    return [
        html.Span("• ", style={"fontSize": "20px", "marginRight": "8px","verticalAlign": "middle"}),
        html.Span(f"{total_revenue:,}",style={"fontSize": "24px","fontWeight":"bold","color": "#00ffcc"}),
        html.Span("Million PKR",style={"fontSize": "16px","marginLeft":"5px"})
    ]

@app.callback(
    Output("research_papers", "children"),
    Input("year_dropdown", "value")
)
def update_research_papers(selected_year):
    filtered_df = df[df["Year"] == selected_year]
    total_papers = filtered_df["Research_Papers"].sum()
    return [
        html.Span("• ", style={"fontSize": "20px", "marginRight": "8px","verticalAlign": "middle"}),
        html.Span(f"{total_papers:,}", style={"fontSize": "24px","fontWeight":"bold","color": "#00ffcc"}),
        html.Span(f"Research papers published", style={"fontSize": "16px","marginLeft":"5px"})
    ]

if __name__ == "__main__":
    app.run(debug=True)
