import pandas as pd
import numpy as np
import plotly.express as px
import dash


import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from wordcloud import WordCloud, STOPWORDS
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib as mpl
import matplotlib.pyplot as plt

import pathlib
from app import app



# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()


df2 = pd.read_csv(DATA_PATH.joinpath("m5_survey_data_technologies_normalised.csv"))











#BAR PLOTS 


tech_used = pd.DataFrame(df2["LanguageWorkedWith"].value_counts().head(10).reset_index())
tech_used.rename(columns = {tech_used.columns[0]: "Technology"}, inplace = True)
tech_used = tech_used.sort_values('LanguageWorkedWith', ascending=True)

fig = px.bar(tech_used, x = "Technology", y = "LanguageWorkedWith")
fig.update_layout(height=275, width=425, showlegend = False, xaxis_title=None, yaxis_title=None)



datab_used = pd.DataFrame(df2["DatabaseWorkedWith"].value_counts().head(10).reset_index())
datab_used.rename(columns = {datab_used.columns[0]: "Database"}, inplace = True)
datab_used = datab_used.sort_values("DatabaseWorkedWith", ascending=True)

fig1 = px.bar(datab_used, x = "Database", y = "DatabaseWorkedWith", color_discrete_sequence =["tomato"]*len(datab_used))
fig1.update_layout(height=275, width=425, showlegend = False, xaxis_title=None, yaxis_title=None)











#WORD CLOUD PLOT

#riparare wordcloud https://github.com/amueller/word_cloud/issues/134

platform_used = pd.DataFrame(df2["PlatformWorkedWith"])
platform_used = platform_used.dropna()


stopwords = set(STOPWORDS)


platform_wc = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(" ".join(platform_used["PlatformWorkedWith"]))

# generate the word cloud
#platform_wc.generate(platform_used[0])

a = plt.figure(figsize = (8, 8), facecolor = None)
#plt.imshow(platform_wc)
#plt.axis("off")
#plt.tight_layout(pad = 0)

platform_wc.to_file('IBMwordcloud.jpg')










#BUBBLE PLOT


web_des = pd.DataFrame(df2["WebFrameWorkedWith"].value_counts().head(10).reset_index())
web_des.rename(columns = {web_des.columns[0]: "WebFrame", web_des.columns[1]:"WebWorked"}, inplace = True)
web_des = web_des.sort_values("WebWorked", ascending=True)

fig2 = px.scatter(web_des, x="WebWorked", y="WebFrame",
	             size="WebWorked", color="WebWorked", color_continuous_scale=px.colors.sequential.RdBu,
                 hover_name="WebFrame", log_x=True, size_max=60,
                 labels= False)

fig2.update_layout(yaxis_title=None)
fig2.update_layout(height=635, width=540)


















#DASH APP

#app = JupyterDash(__name__, external_stylesheets=[dbc.themes.SLATE],
#                meta_tags=[{'name': 'viewport',
#                            'content': 'width=device-width, initial-scale=1.0'}]
#                )

layout = dbc.Container([
    html.Div([
        dbc.Row(
            dbc.Card([
                dbc.Col([
                    html.H1("TECHNOLOGIES USAGE",
                            style={"color": "#CCCCCC", "font-size":40},
                            className='text-left text-light mb-1'),
                    html.H5("The most used technologies, as for StackOverflow's 2019 survey.",
                            style={"color": "#CCCCCC","font-size":15},
                            className='text-left text-light mb-4'),
                ], width=10)
            ], style={"width": 1200})
        ),

        html.Br()
    ]),

    html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    html.Div([
                        dbc.Toast([
                            dcc.Graph(
                                figure=fig.update_layout(
                                    template='plotly_dark',
                                    plot_bgcolor='rgba(0, 0, 0, 0)',
                                    paper_bgcolor='rgba(0, 0, 0, 0)',
                                ),
                                config={
                                    'displayModeBar': False
                                }
                            ),
                        ], header="TOP 10 LANGUAGES WORKED WITH", header_style = {"font-size":20},style={"width": 450})
                    ])
                ]),
                html.Br(),
                dbc.Row([
                    html.Div([
                        dbc.Toast([
                            dcc.Graph(
                                figure=fig1.update_layout(
                                    template='plotly_dark',
                                    plot_bgcolor='rgba(0, 0, 0, 0)',
                                    paper_bgcolor='rgba(0, 0, 0, 0)',
                                ),
                                config={
                                    'displayModeBar': False
                                }
                            ),
                        ], header="TOP 10 DATABASES WORKED WITH", header_style = {"font-size":20},style={"width": 550})
                    ])
                ])
            ], width = 5),
            dbc.Col([
                html.Div([

                    dbc.Toast([
                        dcc.Graph(
                            figure=fig2.update_layout(
                                template='plotly_dark',
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)',
                            ),
                            config={
                                'displayModeBar': False
                            }
                        ),
                    ], header="TOP 10 WEBFRAMES WORKED WITH", header_style = {"font-size":20}, style={"width": 700}
                    )

                ], className="h-100 p-0 text-white bg-dark rounded-3")
            ], width = 7)
        ], justify="between")
    ]),

    html.Div([
        dbc.Row([
            dbc.Col([
                html.Br(),
                dbc.Toast([
                    dbc.Card([
                        dbc.CardImg(
                            src="https://media.giphy.com/media/SwnlsLM41sxZ9BRYec/giphy.gif",
                            alt="nada",
                            class_name="img-thumbnail"),
                    ])
                ], header="MOST USED PLATFORMS", header_style = {"font-size":20}, style={"width" : 400})
            ], width={'size': 4, 'offset': 0}),

            dbc.Col([
                html.Div([
                    html.Br(),
                    dbc.Toast([
                        html.P([
                            "From the survey it is clear that in every group of technologies there are some with significately more usage than the rest (even in the top 10).",
                            html.Br(),
                            html.Br(),
                            "In the Programming Languages bar chart we can see that SQL, HTML/CSS and JavaScript are the preferred languages, almost doubling in usage Bash/Shell/PowerShell (n° 4).",
                            html.Br(),
                            html.Br(),
                            "In the Databases bar chart we can see that PostgreSQL, Microsoft SQL Server and MySQL Server are the preferred databases, presenting by far more usage than their counterparts.",
                            html.Br(),
                            html.Br(),
                            "In the Webframe bubble plot we can see that ASP.NET, React.js, Angular/Angular.js and jQuery are the preferred webframes, achieving a significant margin from the other webframes.",
                            html.Br(),
                            html.Br(),
                            "And lastly in the Platforms wordcloud we can see that Linux, Mac OS, and AWS Docker are the most relevant platforms in terms of usage."
                        ])
                    ], header="SUMMARY", header_style = {"font-size":20},style={"width" : 1000, "color":"#CCCCCC", "font-size":13})
                ])
            ], width={'size': 8}),
        ])
    ])
])