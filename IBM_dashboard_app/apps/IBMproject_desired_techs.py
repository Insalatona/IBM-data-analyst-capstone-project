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
datab_des = pd.DataFrame(df2["LanguageDesireNextYear"].value_counts().head(10).reset_index())
datab_des.rename(columns = {datab_des.columns[0]: "Lenguage"}, inplace = True)
datab_des = datab_des.sort_values("LanguageDesireNextYear", ascending=True)

fig21 = px.bar(datab_des, x = "Lenguage", y = "LanguageDesireNextYear")
fig21.update_layout(height=275, width=425, showlegend = False, xaxis_title=None, yaxis_title=None)




datab_des = pd.DataFrame(df2["DatabaseDesireNextYear"].value_counts().head(10).reset_index())
datab_des.rename(columns = {datab_des.columns[0]: "Database"}, inplace = True)
datab_des = datab_des.sort_values("DatabaseDesireNextYear", ascending=True)

fig22 = px.bar(datab_des, x = "Database", y = "DatabaseDesireNextYear", color_discrete_sequence =["tomato"]*len(datab_des))
fig22.update_layout(height=275, width=425, showlegend = False, xaxis_title=None, yaxis_title=None)

















#WORD CLOUD PLOT

#riparare wordcloud https://github.com/amueller/word_cloud/issues/134

platform_des = pd.DataFrame(df2["PlatformDesireNextYear"])
platform_des = platform_des.dropna()


stopwords = set(STOPWORDS)


platform_wc1 = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(" ".join(platform_des["PlatformDesireNextYear"]))

# generate the word cloud
#platform_wc.generate(platform_used[0])

a = plt.figure(figsize = (8, 8), facecolor = None)
#plt.imshow(platform_wc)
#plt.axis("off")
#plt.tight_layout(pad = 0)

platform_wc1.to_file('IBMwordcloud1.jpg')
















#BUBBLE CHART
web_des = pd.DataFrame(df2["WebFrameDesireNextYear"].value_counts().head(10).reset_index())
web_des.rename(columns = {web_des.columns[0]: "WebFrame", web_des.columns[1]:"WebDes"}, inplace = True)
web_des = web_des.sort_values("WebDes", ascending=True)

fig24 = px.scatter(web_des, x="WebDes", y="WebFrame",
	             size="WebDes", color="WebDes", color_continuous_scale=px.colors.sequential.RdBu,
                 hover_name="WebFrame", log_x=True, size_max=60,
                 labels= False)

fig24.update_layout( yaxis_title=None)
fig24.update_layout(height=635, width=540)






























layout = dbc.Container([
                html.Div([
                    dbc.Row(
                        dbc.Card([
                            dbc.Col([
                                html.H1("FUTURE TECHNOLOGIES TRENDS",
                                        style = {"color":"#CCCCCC", "font-size":40},
                                    className='text-left text-light mb-1'),
                                html.H5("The most sought-after technologies, as for StackOverflow's 2019 survey.",
                                        style = {"color":"#CCCCCC", "font-size":15},
                                        className='text-left text-light mb-4'),
                            ], width = 10)
                        ], style = {"width" : 1200})
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
                                        figure=fig21.update_layout(
                                            template='plotly_dark',
                                            plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                            paper_bgcolor= 'rgba(0, 0, 0, 0)',
                                        ),
                                        config={
                                            'displayModeBar': False
                                        }
                                    ),
                                ], header="TOP 10 DESIRED LANGUAGES", header_style = {"font-size":20},style = {"width" : 600}
                                )
                            ])
                        ]),
                        html.Br(),
                        dbc.Row([
                            html.Div([
                                dbc.Toast([
                                    dcc.Graph(
                                            figure=fig22.update_layout(
                                                template='plotly_dark',
                                                plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                                paper_bgcolor= 'rgba(0, 0, 0, 0)',
                                            ),
                                            config={
                                                'displayModeBar': False
                                            }
                                        ),
                                    ], header="TOP 10 DESIRED DATABASES", header_style = {"font-size":20},style = {"width" : 600}
                                )
                            ])
                        ])
                    ], width = 5),
                    dbc.Col([
                        html.Div([
                            dbc.Toast([
                                dcc.Graph(
                                        figure=fig24.update_layout(
                                            template='plotly_dark',
                                            plot_bgcolor= 'rgba(0, 0, 0, 0)',
                                            paper_bgcolor= 'rgba(0, 0, 0, 0)',
                                        ),
                                        config={
                                            'displayModeBar': False
                                        }
                                    ),
                                ], header="TOP 10 DESIRED WEBFRAMES", header_style = {"font-size":20},style = {"width" : 650}
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
                                    src="https://media.giphy.com/media/xTLSXBXr6jwyDKUTrk/giphy.gif",
                                    alt="nada",
                                    class_name="img-thumbnail"),
                            ])
                        ], header="MOST DESIRED PLATFORMS", header_style={"font-size": 20}, style={"width": 400})
                    ], width={'size':4, 'offset':0}),

                    dbc.Col([
                        html.Div([
                            html.Br(),

                            dbc.Toast([
                               html.P([
                                "From the survey we can see that the most desired technologies demand isn't always met with a corresponding amount of supply. ",
                                html.Br(), 
                                html.Br(),
                                "In the Programming Languages bar chart we can see that beside JavaScript and HTML/CSS there is a discrepancy in the languages offered and demanded in the market.",
                                html.Br(),
                                html.Br(),
                                "In the Databases bar chart we can see that the most demanded database are PostgreSQL and MongoBD, completely different from what the most used databases are.",
                                html.Br(),
                                html.Br(),
                                "In the Webframe bubble plot we can see that leader in demand for the market is React.js and Vue.js, only in the 3rd and 7th position respectively for the most used webrafems.",
                                html.Br(),
                                html.Br(),
                                "And lastly in the Platforms wordcloud we can see that Rasberry PI, Google Cloud and AWS Docker are the most desired platforms."
                            ])
                            ], header="SUMMARY", header_style={"font-size": 20}, style = {"width" : 1000, "color":"#CCCCCC", "font-size":13})

                        ])
                    ], width={'size':8}),
                ])
            ])
        ])
