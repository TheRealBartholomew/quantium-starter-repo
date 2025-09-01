import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

df = pd.read_csv('formatted_data.csv')

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

fig = px.line(
    df,
    x='date',
    y='sales',
    title='Sales of Pink Morsel Over Time',
    labels={'date': 'Date', 'sales': 'Sales (£)'}
)

fig.add_vline(
    x=pd.Timestamp('2021-01-15'),
    line_dash='dash',
    line_color='red'
)

fig.add_annotation(
    x=pd.Timestamp('2021-01-15'),
    y=df['sales'].max(),
    text='Price Increase',
    showarrow=True,
    arrowhead=2
)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Soul Foods Sales Visualiser', style={'textAlign': 'center'}),
    dcc.Graph(
        id='sales-line-chart',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)
