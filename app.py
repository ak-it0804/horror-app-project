import dash
import dash_bootstrap_components as dbc
from dash import html
# import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np
import cv2
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

# img = cv2.imread("./img/0000-1234.png")
# fig_img = px.imshow(img)

df = pd.read_csv("output/kaidan_video_info.csv")
df = df[df["duration"] >= 60].copy()

df_bar = df.groupby("channelTitle").sum()["viewCount"].reset_index().sort_values("viewCount", ascending=False)

fig_bar = go.Figure(
    data=[go.Bar(
    x=df_bar["channelTitle"],
    y=df_bar["viewCount"])]
)

fig_bar.update_layout(
    width=1300,
    height=450,
    margin=dict(l=30, r=10, t=10, b=10),
    paper_bgcolor="rgba(0,0,0,0)",
)

top_view_video = df[["title", "channelTitle", "viewCount"]].head(20)

fig_table = ff.create_table(top_view_video, height_constant=20)
fig_table = go.Figure(
    go.Table(
        header=dict(
            values=top_view_video.columns,
            align="left",
            # line_color=line_color,
            # fill_color=h_fill_color,
            # font_color=font_color,
        ),
        cells=dict(
            values=top_view_video.values.T,
            align="left",
            height=30,
            # line_color=line_color,
            # fill_color=c_fill_color,
            # font_color=font_color,
        ),
        columnwidth = [2,1,0.5]
    )
)

fig_table.update_layout(
    width=1000,
    height=350,
    margin=dict(l=30, r=10, t=10, b=10),
    paper_bgcolor="rgba(0,0,0,0)",
)


sidebar = html.Div(
    [
        dbc.Row(
            html.P("Youtube ホラーチャンネルダッシュボード",
            style={"margin-top": "8px", "margin-bottom": "4px"},
            className="font-weight-bold"),
            
            style={"height": "5vh", "margin": "8px"}
        ),
        dbc.Row(
            [
                html.P("今日のAIが作ったホラー画像",
                style={"margin-top": "8px", "margin-bottom": "4px"}),
                html.Img(src='./image/00030-3622869960.png',
                    height=200,
                    width=200),
            ],
            style={"height": "45vh", "margin": "8px"}
        ),
        dbc.Row(
            html.P("Content C",
            style={"margin-top": "8px", "margin-bottom": "4px"}),
            style={"height": "50vh", "margin": "8px"}
        )
    ]
)

content = html.Div(
    [
        dbc.Row(
            [
                html.P("再生数の多い動画",
                style={"margin-top": "8px", "margin-bottom": "4px"},
                className="font-weight-bold"),
                dcc.Graph(figure=fig_table),
            ],
            style={"height": "50vh","margin-top": "16px", "margin-left": "8px", "margin-bottom": "8px", "margin-right": "8px"}
        ),
        dbc.Row(
            [
                html.P("再生数上位動画のチャンネル別投稿数",
                style={"margin-top": "8px", "margin-bottom": "4px"},
                className="font-weight-bold"),
                dcc.Graph(figure=fig_bar),
            ],
            style={"height": "50vh","margin": "8px"}
        ),         
    ]
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className="bg-light"),
                dbc.Col(content, width=9)
            ],
            style={"height": "100vh"}
        )
    ],
    fluid=True
)


if __name__ == "__main__":
    app.run_server(debug=True, port=1234)