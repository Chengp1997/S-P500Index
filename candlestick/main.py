# plot on dash
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

app.layout = html.Div([
    html.H4('S&P 500 index candlestick chart'),
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider',
                  'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"),
    Input("toggle-rangeslider", "value"))
def display_candlestick(value):
    sp500 = yf.Ticker('^GSPC')
    sp500_hist = sp500.history(period='2y')
    sp500_hist['MA50'] = sp500_hist.Close.rolling(50).mean()
    sp500_hist['MA200'] = sp500_hist.Close.rolling(200).mean()
    fig = go.Figure(data = [go.Candlestick(name="CandleStick",
                       x=sp500_hist.index,
                       open=sp500_hist['Open'],
                       high=sp500_hist['High'],
                       low=sp500_hist['Low'],
                       close=sp500_hist['Close']),
        go.Scatter(name="MA50", x=sp500_hist.index, y=sp500_hist.MA50, line=dict(color='orange', width=1)),
        go.Scatter(name="MA200", x=sp500_hist.index, y=sp500_hist.MA200, line=dict(color='green', width=1))]
        )

    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value
    )

    return fig


app.run_server(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
