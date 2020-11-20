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
input_insight = [
    html.H1("Insights"),
    html.Br(),
    dcc.Markdown(
        """
        ### Limitations
      
        Although the model is superb; nothing is perfect and this model has an accuracy of `±$15`. In addition, estimated
        price for a desired unit on Airbnb may be different due to the age of  the learning dataset. When the bright 
        engineers behind this magnificent model contrived their learned-predictor; a dataset from 2018 was used. The age
        of the dataset does not factor in our cataclysmic event that was 2020, nor does it 'know' about the economic and currency
        fluctuations as a result. Results from this model should serve as a very general baseline to estimate price.
        
        
        ### Process
        
        Using [Britta Bettendorf's "Berlin Airbnb Data"](https://www.kaggle.com/brittabettendorf/berlin-airbnb-data),
        which posses Airbnb listings from Berlin in November of 2018,
        [Robert Giuffre](https://github.com/rgiuffre90) and [Rebecca Duke Wiesenberg](https://github.com/rdukewiesenb)
        both created a model that could predict the price of a hypothetical listing. Predictions are based off of two features
        found in the data: `Property Type` and `Listing Description`. Before making predictions, our intrepid engineers
        split the data into two piles of data--train and test (80/20). Training was conducted with the aptly named
        'train' data subset and tested the model's scores against the other aptly named 'test' data subset. Their model
        is comprised of two neural networks; wide model and a deep model. Wide neural model provides the breadth needed
        to properly evaluate the data while the deep model does text analysis on the listing description.
        """)
]
layout = dbc.Col(input_insight)
