# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Model pip installs
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
import joblib
from keras.models import load_model

from joblib import load
tokenizer = load('assets/tokenizer.joblib')
encoder = joblib.load('assets/label_encoder.joblib')
combined = load_model('assets/best_model.h5')

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
input_block = dbc.FormGroup(
    [
        dbc.Label("Property Type"),
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
            value='Loft',  # default value
            multi=False,
            style={'margin': 'auto'}
        ),
        dbc.FormText("Pick one."),
        html.Br(),
        dbc.Label("What are you looking for?"),
        dbc.Textarea(
            invalid=False,
            bs_size="sm",
            id='amenities',
            value="Has 2 bedrooms, patio and WiFi internet. Prefer first floor and no stairs with a view of the ocean.",
            style={'margin': 'auto'},
        ),
        dbc.FormText("Write in what you'd like, in English or German!"),
        html.Br(),
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Submit',
            className='mr-1',
            color="success",
            block=True,
            outline=False,
            active=True
        ),
    ],
    style={'align': 'left', 'width': '50%'},
    className=['ml-2', 'mb-2', 'mt-2']
)

row = html.Div(
    [
        dbc.Row(dbc.Col(
            html.Div(
                html.H1("Single Column"),
                style={'align': 'center'}
            ))
        ),
        dbc.Row(
            [
                dbc.Col((html.Div(input_block))),
                dbc.Col([
                    html.H1("Expected Price"),
                    html.Div(id='prediction-content')
                ])
            ]
        )
    ]
)

@app.callback(
    Output('prediction-content', 'children'),
    [Input('dropdown', 'value'), Input('amenities', 'value')],
)
def predict(dropdown, amenities):
    property_type = []
    property_type.append(dropdown)
    description_text = amenities
    building = encoder.transform(property_type)
    building = keras.utils.to_categorical(building, 13)

    max_seq_length = 170
    embed = tokenizer.texts_to_sequences(description_text)
    embed = keras.preprocessing.sequence.pad_sequences(
        embed, maxlen=max_seq_length, padding="post")

    description_bow = tokenizer.texts_to_matrix(description_text)
    building_transform = [list(building[0]) for n in range(description_bow.shape[0])]
    building = np.array(building_transform)

    predictions = combined.predict([description_bow, building] + [embed])
    val = predictions[0]

    return f'The estimated rent is ${"{:.2f}".format(val[0])} per night.'


layout = row
