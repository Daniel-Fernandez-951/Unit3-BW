# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
input_block = dbc.FormGroup(
    [
        html.H6('Property Type', style={
            'textAlign': 'center'
        }),
        dcc.Dropdown(
            id='dropdown',
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
            placeholder='Loft',  # default value
            multi=False,
            style={'margin': 'auto'}
        ),
        html.Br(),
        html.H6('Write in Amenities', style={
            'textAlign': 'center'
        }),
        dbc.Textarea(
            invalid=False,
            bs_size="sm",
            id='amenities',
            placeholder="Example:\n"
                        "A loft with 2 bedrooms, patio and WiFi internet. "
                        "Prefer first floor and no stairs with a view of the ocean.",
            style={'margin': 'auto'},
        ),
        html.Br(),
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            className='mr-1',
            color="success",
            block=True,
            outline=False
        ),
    ],
    style={'align': 'left', 'width': '33%'}
)

layout = dbc.Col(input_block)
