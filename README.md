# A Night in Berlin: Predicting Airbnb prices in Berlin

## Authors: Rebecca Duke Wiesenberg, Daniel Fernandez, Robert Giuffre

## Dash template

[Dash Template](https://lambdaschool.github.io/ds/unit2/dash-template/)

## Kaggle dataset that project is based off of
[Kaggle Dataset] (https://www.kaggle.com/brittabettendorf/berlin-airbnb-data?select=listings_summary.csv)

## Methdology
Based on Britta Bettendorf's kaggle data "Berlin Airbnb Data", which contains information about Airbnb listings in Berlin, Germany in November 2018, we created a model that could predict the price of a hypothetical listing.

We chose to base our predictions off of two elements of an Airbnb listing: type of property and listing description.

In order to analyze and make predictions from the data, we first split the data into training (80 percent) and testing (20 percent) subdatasets. We fed the models the training data, and then tested the model's scores against the testing data.

Our model is composed of two neural networks: a wide model and a deep model. The wide model provides the breadth needed to do a proper evaluation of the data. The deep model, with its embedding layers, does the deep text analysis of the listing descriptions.

## Insights
Model should have a margin of error of $15. However, it should be noted that the model is not 100 percent accurate, since it does not take into account any currency fluctuations, nor the coronavirus pandemic.
