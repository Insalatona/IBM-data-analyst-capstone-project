import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
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


df1 = pd.read_csv(DATA_PATH.joinpath("m5_survey_data_demographics.csv"))

















#pie chart

respond_gen = pd.DataFrame(df1["Gender"].value_counts().reset_index())
respond_gen.rename(columns = {respond_gen.columns[0]: "Gender", respond_gen.columns[1]:"Tot"}, inplace = True)
respond_gen = respond_gen.replace({"Gender" : {"Man;Non-binary, genderqueer, or gender non-conforming": "Man non-conforming",
                                    "Woman;Non-binary, genderqueer, or gender non-conforming": "Woman non-conforming", 
                                    "Woman;Man;Non-binary, genderqueer, or gender non-conforming": "Woman;Man; non-conforming",
                                    "Non-binary, genderqueer, or gender non-conforming" : "Other non-conforming",}}, regex=True)                                                               

fig31 = px.pie(respond_gen, values = "Tot", names = "Gender", hole=.6, color_discrete_sequence=px.colors.sequential.RdBu)
fig31.update_layout(height=400, width = 450, legend=dict(
    yanchor="top",
    y=0.7,
    xanchor="left",
    x=-0.99,
    font=dict(size= 11.5)))
















#WORD CLOUD PLOT

#riparare wordcloud https://github.com/amueller/word_cloud/issues/134

resp_country = pd.DataFrame(df1["Country"])
resp_country = resp_country.dropna()
resp_country = resp_country.replace(' ', '_', regex=True)



stopwords = set(STOPWORDS)
resp_country = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(" ".join(resp_country["Country"]))

# generate the word cloud
#platform_wc.generate(platform_used[0])

a = plt.figure(figsize = (8, 8), facecolor = None)
#plt.imshow(platform_wc)
#plt.axis("off")
#plt.tight_layout(pad = 0)

resp_country.to_file('IBMwordcloud2.jpg')

#gify link
#https://media.giphy.com/media/ymxewgtkgfvTkUW27q/giphy.gif

















#LINE POT

resp_age = df1[["Respondent", "Age"]].groupby("Age").count().reset_index()
resp_age.rename(columns = {resp_age.columns[1]:"Tot Respondets"}, inplace = True)

fig33 = px.line(resp_age, x = "Age", y = "Tot Respondets")
fig33.update_traces(line_color='coral')
fig33.update_layout(height=400)














#STACKED BAR CHART
respond_ed = df1[["Respondent", "Gender", "EdLevel"]].groupby(["EdLevel", "Gender"]).count().reset_index()

respond_ed = respond_ed.replace({"Gender" : {"Man;Non-binary, genderqueer, or gender non-conforming": "Man non-conforming",
                                    "Woman;Non-binary, genderqueer, or gender non-conforming": "Woman non-conforming", 
                                    "Woman;Man;Non-binary, genderqueer, or gender non-conforming": "Woman;Man; non-conforming",
                                    "Non-binary, genderqueer, or gender non-conforming" : "Other non-conforming",}})

respond_ed = respond_ed.replace({"EdLevel" : {"Bachelor’s degree (BA, BS, B.Eng., etc.)": "Bachelor",
                                    "Master’s degree (MA, MS, M.Eng., MBA, etc.)": "Master", 
                                    "Some college/university study without earning a degree": "College, no degree",
                                    "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)" : "Secondary school",
                                    "Other doctoral degree (Ph.D, Ed.D., etc.)": "Other doctoral degree",
                                    "Professional degree (JD, MD, etc.)": "Professional degree",
                                    "I never completed any formal education": "No education",
                                    "Primary/elementary school": "Primary school"}})

fig34 = px.bar(respond_ed, x = "Gender", y = "Respondent", color = "EdLevel", color_discrete_sequence=px.colors.sequential.RdBu)
fig34.update_layout(height=320)












layout = dbc.Container([
    html.Div([
        dbc.Row(
            dbc.Card([
                dbc.Col([
                    html.H1("TECHNOLOGIES DEMOGRAPHICS",
                            style = {"color":"#CCCCCC", "font-size":40},
                            className='text-left text-light mb-1'),
                    html.H5(
                        "Demographic composition of the currently most used technologies, as for StackOverflow's 2019 survey.",
                        style={"color": "#CCCCCC", "font-size": 15},
                        className='text-left text-light mb-4'),
                ], width=10)
            ], style={"width": 1200})
        ),

        html.Br()
    ]),

    html.Div([
        dbc.Row([
        dbc.Col([
                html.Div([

                    dbc.Toast([
                        dcc.Checklist(
                            id="my-checklist",
                            options=[{"label": x, "value": x} for x in respond_ed["Gender"].unique()],
                            value=["Man", "Woman"],
                            labelStyle={'display': 'inline-block'},
                            style = {"color":"#CCCCCC", "font-size":15},
                        ),
                        dcc.Graph(id="bar_database")
                    ], header="RESPONDENTS EDUCATION LEVEL GROUPED BY GENDER", style={"width": 800, "height": 465}, header_style={"font-size": 18}
                    )

                ])
            ], width=7),

            dbc.Col([
                html.Div([

                    dbc.Toast([
                        dcc.Graph(
                            figure=fig31.update_layout(
                                template='plotly_dark',
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)',
                            ),
                            config={
                                'displayModeBar': False
                            }
                        ),
                    ], header="RESPONDENTS GENDER", style={"width": 600, "height": 465}, header_style={"font-size": 18}
                    )
                ]),
            ], width=5),



        ]),

        html.Br(),

        dbc.Row([
            dbc.Col([
                html.Div([

                    dbc.Toast([
                        dcc.Graph(
                            figure=fig33.update_layout(
                                template='plotly_dark',
                                plot_bgcolor='rgba(0, 0, 0, 0)',
                                paper_bgcolor='rgba(0, 0, 0, 0)',
                            ),
                            config={
                                'displayModeBar': False
                            }
                        )
                    ], header="RESPONDENTS AGE", style={"width": 1400}, header_style={"font-size": 20}
                    )
                ], className="h-100 p-0 text-white bg-dark rounded-3")

            ], width=15)
        ]),
    ]),
])



@app.callback(
            Output(component_id='bar_database', component_property='figure'),
            Input(component_id="my-checklist", component_property='value')
            )

def filter_bar(option_chosen):
    mask = respond_ed["Gender"].isin(option_chosen)

    fig = px.bar(respond_ed[mask], x="Gender", y="Respondent", color="EdLevel",
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(height=360)
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    return fig

