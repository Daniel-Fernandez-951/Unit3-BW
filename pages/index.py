# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Imports from this application
from app import app

# data to be loaded
data = [['Alex', 10], ['Bob', 12], ['Clarke', 13], ['Alex', 100]]
df = pd.DataFrame(data, columns=['Name', 'Mark'])

property_card = dbc.Card(
    [
        dbc.CardHeader("Property Type"),
        dbc.CardBody([
            html.H6("Select Type", className="card-title"),
            dcc.Dropdown(
                id='property_type',
                options=[
                    {'label': 'Apartment', 'value': 'Apartment'},
                    {'label': 'Condominium', 'value': 'Condominium'},
                    {'label': 'Loft', 'value': 'Loft'},
                    {'label': 'House', 'value': 'House'},
                    {'label': 'Serviced Apartment', 'value': 'Serviced apartment'},
                    {'label': 'Hostel', 'value': 'Hostel'},
                    {'label': 'Townhouse', 'value': 'Townhouse'},
                    {'label': 'Guest Suite', 'value': 'Guest suite'},
                    {'label': 'Bed & Breakfast', 'value': 'Bed & breakfast'},
                    {'label': 'Guesthouse', 'value': 'Guesthouse'},
                    {'label': 'Hotel', 'value': 'Hotel'},
                    {'label': 'Other', 'value': 'Other'},
                    {'label': 'Boutique Hotel', 'value': 'Boutique hotel'}

                ],
                value='Loft',
                className='mb-4',
            )
        ])
    ]
)

host_card = dbc.Card(
    [
        dbc.CardHeader("Property Amenities"),
        dbc.CardBody([
            html.H6("Write in Amenities"),
            dbc.Textarea(
                invalid=False,
                bs_size="sm",
                id='amenities',
                placeholder="Example:\n"
                            "A loft with 2 bedrooms, patio and WiFi internet. "
                            "Prefer first floor and no stairs with a view of the ocean.",
                style={'width': '100%', 'height': '80%'},
            )
        ])
    ]
)

layout = dbc.Row([dbc.CardDeck(dbc.Col([property_card, host_card]))])
