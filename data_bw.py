# -*- coding: utf-8 -*-
"""Becky's Copy of BuildWeekUnit4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10YgWQTF1kTEKCDEvfbufw8eJd2ZsAqdv

## Import Statements
"""

import pandas as pd
import numpy as np
import requests
import spacy
import os
import tensorflow as tf

import tensorflow as tf
from tensorflow import keras
from sklearn.pipeline import Pipeline
from tensorflow.keras import Sequential, regularizers
from tensorflow.keras.optimizers import SGD, Adam, Adagrad, Nadam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Flatten, ReLU
from tensorflow.keras.activations import sigmoid, softmax, relu
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard

from spacy.tokenizer import Tokenizer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestNeighbors
from gensim.models import LdaMulticore
from gensim.corpora import Dictionary

from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

import re, string, timeit
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.model_selection import GridSearchCV

# import gensim
# import gensim.corpora as corpora
# from gensim.utils import simple_preprocess
# from gensim.models import CoherenceModel
# import pyLDAvis
# import pyLDAvis.gensim 
import matplotlib.pyplot as plt

"""## Import data"""

PATH = '/content/listings_summary.csv'

listings = pd.read_csv(PATH, index_col='id')

listings.head()

listings.columns

"""## Feature Engineering"""

'''
INDEX:
id

property_type
beds
bathrooms
amenities
price
minimum_nights
review_score_rating
neighbourhood_group_cleansed

BINARY:
**host_identity_verified
cleaning_fee
security_deposit

'''

cols = ['beds', 'property_type', 'price', 'description', 
                'minimum_nights', 'review_scores_rating',
                 'neighbourhood_group_cleansed',
                 'host_identity_verified', 'cleaning_fee',
                 'security_deposit']


listings = listings[cols]

listings.head(1)

cols = ['cleaning_fee', 'security_deposit']

# remove '$' and ',' so that we can process a monteary amount 
# as a float, versus an object

listings[cols] = listings[cols].replace({'\$': '', ',': ''}, regex=True).astype(float)

listings['price'] = listings['price'].replace({'\$': '', ',': ''}, regex=True).astype(float)

listings['cleaning_fee']

# create binary column for cleaning fee or not

def binary_fee(x):
  if x > 0.0:
    return "Yes"
  else:
    return "No"

listings['cleaning_fee_binary'] = listings['cleaning_fee'].apply(binary_fee)

listings['cleaning_fee_binary'].value_counts()

listings['security_deposit_binary'] = listings['security_deposit'].apply(binary_fee)

listings['security_deposit_binary'].value_counts()

# dropping monetary columns because it will overwhelm
# our computer later on
drop_cols = ['security_deposit', 'cleaning_fee']

listings = listings.drop(drop_cols, axis=1)

listings.head(2)

"""## NLP and text analysis"""

listings['description'] = listings['description'].astype(str)

listings['property_type'] = listings['property_type'].astype(str)

# downloading the language libraries
# %%capture
# !python -m spacy download en_core_web_md 
# !python -m spacy download de_core_news_md
# !python -m spacy download xx_ent_wiki_sm

# defining each language library
# English
# nlp_en = spacy.load('en_core_web_md')
# German
# nlp_de = spacy.load('de_core_news_md')
# Multi
# nlp_multi = spacy.load('xx_ent_wiki_sm')

"""### Tfidf Vectorizer (if we wanted a non-NN model to do text analysis)"""

# def tokenize(text):
    
#   lemmas = []  
      
#   doc = nlp_en(text)

#   for token in doc:
#     if((token.is_stop == False ) & (token.is_punct == False)):
#         lemmas.append(token.lemma_.lower())

#   return lemmas

# def proccess_text(text):
#   lang = detect_lang(text)
#   sent_langs = []
#   doc = nlp_en(text)
#   for sent in doc.sents:
#     lang_pred = sent._.language['language']
#     lang = 'de' if lang_pred in ['de', 'nl'] else 'en'
#     sent_langs.append((sent.text, lang))
#   processed_text = []
#   for sent in sent_langs:
#     if sent[1] == 'de':
#       tokens = [token.lemma_ for token in nlp_de(sent[0])]
#     else:
#       tokens = [token.lemma_ for token in nlp_en(sent[0])]
#     for token in tokens:
#       processed_text.append(token)
#   return processed_text

# listings['lemmas'] = listings['description'].apply(tokenize)

# listings['amenities'][2]

# vects = [nlp_en(string).vector for string in listings['description']]

# listings['vects'] = vects

# pipe = Pipeline([('tfidf', TfidfVectorizer()), ('clf', KNeighborsClassifier())])

# pipe.fit(listings['description'], listings['price'])

# parameters = {
#     'tfidf__max_df':(0.25, 0.75, 1),
#     'tfidf__ngram_range': [(1, 1), (1, 2), (1, 3)],
    
# }

# grid_search = GridSearchCV(pipe,parameters, cv=5, n_jobs=-1, verbose=1)
# grid_search.fit(listings['description'], listings['price'])

# grid_search.best_score_

# listings['lemmas'][2]

# test = """
# My modern 2-bedroom apartment has everything you need for your Berlin trip. 
# The unit comes with heating, a washer, and free parking.
#  During your stay, you can also enjoy using a convenient gym and kitchen. 
# Our Airbnb is within walking distance to several popular restaurants and shops. 
# An ideal base to explore Berlin.

# """

# grid_search.predict([test])

"""## Data Splitting"""

variety_threshold = 40 # Anything that occurs less than this will be removed.
value_counts = listings['property_type'].value_counts()
to_remove = value_counts[value_counts <= variety_threshold].index
listings.replace(to_remove, np.nan, inplace=True)
listings = listings[pd.notnull(listings['property_type'])]

train_size = int(len(listings) * .8)

# Train features
description_train = listings['description'][:train_size]
variety_train = listings['property_type'][:train_size]

# Train labels
labels_train = listings['price'][:train_size]

# Test features
description_test = listings['description'][train_size:]
variety_test = listings['property_type'][train_size:]

# Test labels
labels_test = listings['price'][train_size:]

"""### Baseline Score"""

print("Description Baseline Score: ", description_train.value_counts(normalize=True).max())

"""## Compiled-Model Neural Network"""

layers = keras.layers

# This code was tested with TensorFlow v1.7
print("You have TensorFlow version", tf.__version__)

listings['property_type'].value_counts()

vocab_size = 6000
tokenize = keras.preprocessing.text.Tokenizer(num_words=vocab_size, char_level=False)
tokenize.fit_on_texts(description_train)

description_bow_train = tokenize.texts_to_matrix(description_train)
description_bow_test = tokenize.texts_to_matrix(description_test)

encoder = LabelEncoder()
encoder.fit(variety_train)
variety_train = encoder.transform(variety_train)
variety_test = encoder.transform(variety_test)
num_classes = np.max(variety_train) + 1

# Convert labels to one hot
variety_train = keras.utils.to_categorical(variety_train, num_classes)
variety_test = keras.utils.to_categorical(variety_test, num_classes)

# Hyperparameter tuning
logdir = os.path.join("logs", "EarlyStopping-loss")
tb_callback = TensorBoard(logdir, histogram_freq=5)
stop = EarlyStopping(monitor='loss',
                     min_delta=0.01845,
                     patience=2)

"""#### Wide Model"""

bow_inputs = layers.Input(shape=(vocab_size,))
variety_inputs = layers.Input(shape=(num_classes,))
merged_layer = layers.concatenate([bow_inputs, variety_inputs])
merged_layer = layers.Dense(256, activation='relu')(merged_layer)
merged_layer = layers.Dense(896, activation='relu')(merged_layer)
predictions = layers.Dense(1)(merged_layer)
wide_model = keras.Model(inputs=[bow_inputs, variety_inputs], outputs=predictions)

wide_model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
print(wide_model.summary())

train_embed = tokenize.texts_to_sequences(description_train)
test_embed = tokenize.texts_to_sequences(description_test)

max_seq_length = 170
train_embed = keras.preprocessing.sequence.pad_sequences(
    train_embed, maxlen=max_seq_length, padding="post")
test_embed = keras.preprocessing.sequence.pad_sequences(
    test_embed, maxlen=max_seq_length, padding="post")

"""### Deep Model"""

deep_inputs = layers.Input(shape=(max_seq_length))
# input layer
embedding = layers.Embedding(vocab_size, 8, input_length=max_seq_length)(deep_inputs)

# hidden layers
embedding = layers.Flatten()(embedding)
# model = tf.expand_dims(embed_out, axis=-1)
# embed_out = layers.Dense(10, activation="relu")(embedding)
embed_out = layers.Dense(256, activation="relu")(embedding)
embed_out = layers.Dense(896, activation="relu")(embedding)
embed_out = layers.Dense(1)(embedding)

# output layer
deep_model = keras.Model(inputs=deep_inputs, outputs=embed_out)
print(deep_model.summary())

deep_model.compile(loss='mse',
                       optimizer='adam',
                       metrics=['accuracy'])

"""### Combined Model"""

merged_out = layers.concatenate([wide_model.output, deep_model.output])
merged_out = layers.Dense(10, activation="relu")(merged_out)
merged_out = layers.Dense(256, activation="relu")(merged_out)
merged_out = layers.Dense(896)(merged_out)
combined_model = keras.Model(wide_model.input + [deep_model.input], merged_out)
print(combined_model.summary())

combined_model.compile(loss='mse',
                       optimizer='adam',
                       metrics=['accuracy'])

combined_model.fit([description_bow_train, variety_train] + [train_embed], 
                   labels_train, epochs=20, batch_size=40, 
                   verbose=2, callbacks=[stop])

"""### Evaluating the Combined Model and Making Predictions"""

combined_model.evaluate([description_bow_test, variety_test] + [test_embed], 
                        labels_test, batch_size=40, verbose=2)

predictions = combined_model.predict([description_bow_test, variety_test] + [test_embed])

num_predictions = 40
diff = 0

for i in range(num_predictions):
    val = predictions[i]
    print(description_test.iloc[i])
    print('Predicted: ', val[0], 'Actual: ', labels_test.iloc[i], '\n')
    diff += abs(val[0] - labels_test.iloc[i])

print('Average prediction difference: ', diff / num_predictions)

"""## Pickling Model"""

import pickle
from pickle import dump

from keras.models import load_model

combined_model.save('best_model.h5')



"""## Miscellanous Code from Experimentation Stage"""

####################

# train_size = int(len(listings) * .8)

# # Train features
# description_train = listings['description'][:train_size]
# # variety_train = listings['test_amenities'][:train_size]

# # Train labels
# labels_train = listings['price'][:train_size]

# # Test features
# description_test = listings['description'][train_size:]
# # variety_test = listings['test_amenities'][train_size:]

# # Test labels
# labels_test = listings['price'][train_size:]

# vocab_size = 20000
# tokenize = keras.preprocessing.text.Tokenizer(num_words=vocab_size, char_level=False)
# tokenize.fit_on_texts(description_train)

# description_bow_train = tokenize.texts_to_matrix(description_train)
# description_bow_test = tokenize.texts_to_matrix(description_test)

# # Hyperparameter tuning
# logdir = os.path.join("logs", "EarlyStopping-loss")
# tb_callback = TensorBoard(logdir, histogram_freq=3)
# stop = EarlyStopping(monitor='loss',
#                      min_delta=0.0184,
#                      patience=2)

# train_embed = tokenize.texts_to_sequences(description_train)
# test_embed = tokenize.texts_to_sequences(description_test)

# max_seq_length = 250
# train_embed = keras.preprocessing.sequence.pad_sequences(
#     train_embed, maxlen=max_seq_length, padding="post")
# test_embed = keras.preprocessing.sequence.pad_sequences(
#     test_embed, maxlen=max_seq_length, padding="post")

# deep_inputs = layers.Input(shape=(max_seq_length))
# # input layer
# embedding = layers.Embedding(vocab_size, 15, input_length=max_seq_length)(deep_inputs)

# # hidden layers
# embedding = layers.Flatten()(embedding)
# embed_out = layers.Dense(1)(embedding)
# # model = tf.expand_dims(embed_out, axis=-1)
# embed_out = layers.LSTM(32, activation="relu")
# embed_out = layers.Dense(52, activation="relu")(embedding)
# embed_out = layers.Dense(256, activation="relu")(embedding)
# # embed_out = layers.Dense(256, activation="relu")(embedding)


# # output layer
# embed_out = layers.Dense(896, activation="relu")(embedding)
# deep_model = keras.Model(inputs=deep_inputs, outputs=embed_out)
# print(deep_model.summary())

# deep_model.compile(loss='mse',
#                        optimizer='adam',
#                        metrics=['accuracy'])

# deep_model.fit(train_embed,
#               labels_train, epochs=20, batch_size=32,
#                callbacks=[tb_callback, stop],
#                verbose=2)

# deep_model.evaluate(test_embed, 
#                     labels_test, 
#                     batch_size=250, verbose=2)

# predictions1 = deep_model.predict([test_embed])

# num_predictions = 40
# diff = 0

# for i in range(num_predictions):
#     val = predictions1[i]
#     print(description_test.iloc[i])
#     print('Predicted: ', val[0], 'Actual: ', labels_test.iloc[i], '\n')
#     diff += abs(val[0] - labels_test.iloc[i])

###############################

# merged_out = layers.concatenate([wide_model.output, deep_model.output])
# merged_out = layers.Dense(1)(merged_out)
# combined_model = keras.Model(wide_model.input + [deep_model.input], merged_out)
# print(combined_model.summary())

# combined_model.compile(loss='mse',
#                        optimizer='nadam',
#                        metrics=['accuracy'])

# combined_model.fit([description_bow_train, variety_train] + [train_embed], 
#                    labels_train, epochs=20, batch_size=32, 
#                     callbacks=[tb_callback, stop], verbose=2)

# deep_model.evaluate([description_bow_test, variety_test] + [test_embed], 
#                         labels_test, batch_size=128, verbose=2)

# predictions = deep_model.predict([description_bow_test, variety_test] + [test_embed])

# num_predictions = 40
# diff = 0

# for i in range(num_predictions):
#     val = predictions[i]
#     print(description_test.iloc[i])
#     print('Predicted: ', val[0], 'Actual: ', labels_test.iloc[i], '\n')
#     diff += abs(val[0] - labels_test.iloc[i])

# from tensorflow.keras.models import Sequential

# from tensorflow.keras.optimizers import SGD, Adam, Adadelta, Adagrad, Adamax, Ftrl, Nadam
# from tensorflow.keras.layers import Dense
# import tensorflow.keras.backend as K
# import tensorflow as tf



# def customize_relu(alpha):
#   return lambda x: tf.keras.activations.relu(x, alpha=alpha)

# def create_model(hp):


#   model = Sequential()

#   hp_units = hp.Int('units', 32, 512, 32)
  
#   alphas  = hp.Float('relu_alphas', 0.0, 0.1, 0.02)
  
#   for i in range(hp.Int('num_layers', 2, 20)):
#     model.add(Dense(units=hp_units,
#                     activation=customize_relu(alphas)))
    
#   lrs = hp.Choice('learning_rate',
#                    values=[.001, .01, .1]
#                   )
#   optimizer_choices = hp.Choice('optimizer',
#                                 ['Adadelta', 'Adagrad',
#                                   'Adamax', 'Ftrl', 'Nadam'])
   
#   optimizer = eval(f'{optimizer_choices}(learning_rate={lrs})')
  

#   model.add(Dense(10, activation='softmax'))


#   # model compiling
#   model.compile(optimizer=optimizer,
#                 loss='sparse_categorical_crossentropy',
#                 metrics=['accuracy'])

#   return model

# !pip install keras-tuner

# from tensorflow import keras
# from tensorflow.keras import layers
# from kerastuner.tuners import RandomSearch

# !pip install category_encoders
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# import seaborn as sns
# from sklearn.impute import SimpleImputer
# from sklearn.metrics import accuracy_score
# from sklearn.model_selection import train_test_split
# from sklearn.pipeline import make_pipeline
# from sklearn.ensemble import RandomForestClassifier
# from category_encoders import OneHotEncoder, OrdinalEncoder
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.feature_selection import SelectKBest
# from sklearn.model_selection import GridSearchCV
# from sklearn.ensemble import RandomForestClassifier

# X_train = listings.drop(['price', 'description', 'amenities'], axis=1)[:train_size]

# y_train = listings['price'][:train_size]

# X_test = listings.drop(['price', 'description', 'amenities'], axis=1)[train_size:]
# y_test = listings['price'][train_size:]

# model = make_pipeline(
#     OneHotEncoder(use_cat_names=True),
#     SimpleImputer(),
#     DecisionTreeClassifier(random_state=42)
# )

# model.fit(X_train, y_train);

# training_acc = model.score(X_train, y_train)
# validation_acc = model.score(X_test, y_test)
# print('Training Accuracy Score:', training_acc)
# print('Validation Accuracy Score:', validation_acc)

# tuner = RandomSearch(
#     create_model,
#     objective='val_accuracy',
#     max_trials=5,
#     executions_per_trial=3,
#     directory='./',
#     project_name='final')

# tuner.search_space_summary()

# tuner.search(X_train, y_train,
#              epochs=5,
#              validation_data=(X_test, y_test))