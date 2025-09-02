# dash_sales_app.py
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load sales data
df = pd.read_csv('formatted_data.csv')

# Ensure 'date' is datetime and sort
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Initialise Dash app
app = dash.Dash(__name__)

# App layout with styling
app.layout = html.Div([
    html.H1(
        'Soul Foods Sales Visualiser',
        style={
            'textAlign': 'center',
            'color': '#2c3e50',
            'fontFamily': 'Arial, sans-serif',
            'marginBottom': '20px'
        }
    ),

    html.Div([
        html.Label(
            "Filter by Region:",
            style={'fontWeight': 'bold', 'marginRight': '10px'}
        ),
        dcc.RadioItems(
            id='region-filter',
            options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'},
            ],
            value='all',
            inline=True,
            style={'fontFamily': 'Arial, sans-serif'}
        )
    ], style={
        'textAlign': 'center',
        'marginBottom': '30px',
        'padding': '10px',
        'backgroundColor': '#ecf0f1',
        'borderRadius': '8px',
        'boxShadow': '2px 2px 6px rgba(0,0,0,0.1)',
        'display': 'inline-block'
    }),

    html.Div([
        dcc.Graph(id='sales-line-chart')
    ], style={
        'padding': '20px',
        'backgroundColor': '#ffffff',
        'borderRadius': '12px',
        'boxShadow': '4px 4px 12px rgba(0,0,0,0.15)',
        'maxWidth': '900px',
        'margin': 'auto'
    })
], style={'backgroundColor': '#f9f9f9', 'padding': '20px'})


# Callback to update line chart based on region filter
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    # Filter dataset
    if selected_region == 'all':
        dff = df
    else:
        dff = df[df['region'] == selected_region]

    # Create line chart
    fig = px.line(
        dff,
        x='date',
        y='sales',
        title=f"Sales of Pink Morsel Over Time ({selected_region.capitalize()})",
        labels={'date': 'Date', 'sales': 'Sales (£)'}
    )

    # Add vertical line for price increase
    fig.add_vline(
        x=pd.Timestamp('2021-01-15'),
        line_dash='dash',
        line_color='red'
    )

    # Add annotation
    if not dff.empty:
        fig.add_annotation(
            x=pd.Timestamp('2021-01-15'),
            y=dff['sales'].max(),
            text='Price Increase',
            showarrow=True,
            arrowhead=2
        )

    fig.update_layout(
        plot_bgcolor="#fafafa",
        paper_bgcolor="#fafafa",
        font=dict(family="Arial, sans-serif", size=14, color="#2c3e50"),
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)
