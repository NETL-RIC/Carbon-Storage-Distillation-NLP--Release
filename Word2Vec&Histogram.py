#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 09:06:43 2019

@author: yeatesd, refactored by greenbur
Combination of Word2VecV1 and Histogram
"""

# =============================================================================
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from PDFtoDatabase import cleanupdocuments #Custom Clean Up Module
import SQLite #Custom SQL Query Module
import gzip
import pandas as pd
import matplotlib as plt
import numpy as np
import time
import sys
# =============================================================================
# User variables 
# Location of SQLite database
# =============================================================================
database_location = '/home/greenbur/NLP/Python Code/WorkingPapersGOMlg.sqlite'

# Path where model will be saved
savemodelpath = '/home/greenbur/NLP/Results/GOMlgvec.txt'

# Load document data from database
# connect to swlite database and load data
cursor, conn = SQLite.connect_to_databse(database_location)
datatable = SQLite.list_all_rows(cursor, 'papers')

# Collect paper text and load to python list
paperdata = []
for row in datatable:
    paperdata.append(row[6])

# Clean text for processing
cleandoc = cleanupdocuments(paperdata)
print("Documents loaded and ready to process")

# This section builds the Word2Vec model and saves the model
print("Starting word2vec")

# Build Word2Vec model, params adjjusted for future testing
model = Word2Vec(cleandoc, size = 500, window = 5, min_count = 3, workers = 4,
                 compute_loss = True)

# Create word vectors
word_vectors = model.wv

# Save model to test to import in spacy
model.wv.save_word2vec_format(savemodelpath)
print("Vectors Created")

# =============================================================================
# To build a custom spacy model open a terminal and enter
# Zip output text file to gzip file then run python module
# 'python -m spacy init-model en spacy.XMATvec.model --vectors-loc XMATvec.txt.gz'
# 
# Word2Vec tests, find words similar to 'creep'
# =============================================================================
#print(word_vectors.most_similar(['creep']))

# Compare 2 words
sim = word_vectors.n_similarity(['computer'], ['human'])
print(sim)

# View word vector
print(model['grain'])


#%%
# =============================================================================
# Build a list of the terms, integer indicies,
# and term counts from the food2vec model vocabulary.
# 
# =============================================================================
ordered_vocab = [(term,voc.index, voc.count) for term, voc in model.wv.vocab.items()]

# Sort by the term counts, so the most common terms appear first
ordered_vocab = sorted(ordered_vocab, key = lambda k: -k[2])

# Unzip the terms, integer indices and counts into seperate lists
ordered_terms, term_indices, term_counts = zip(*ordered_vocab)
print("ordered_terms")

# Create a DataFrame with the food2vec vectors as data,
# and the terms as row labels
#word_vectors = pd.DataFrame(model.wv.syn0norm[term_indices, :], index = ordered_terms)

#%% Organize words into panda series -> choose if you want all values or a subset
words = pd.Series(ordered_terms)

# Subset of values n is the number of values run, random_state is to reproduce
# random results with the same vectors and size
wordshort = words.sample(n = 1000, random_state = 50)

# =============================================================================
# If you want all values use the below code
# wordshort = words
# And for a list of specific words use:
# wordshort = pd.Series(['sandstone', 'reservoir', 'oil', 'gas','structure'])
# =============================================================================
#%% Calculate similarities
sim = []
length = wordshort.shape[0]
start_time = time.time()
for i in range(0,length):
    for j in range(i+1,length):
        x = [wordshort.iloc[i]]
        y = [wordshort.iloc[j]]
        z = word_vectors.n_similarity(x,y)
        sim.append([x,y,z])
        #print([wordshort.iloc[i]], [wordshort.iloc[j]])

print("--- {} seconds ---".format(time.time() - start_time))

#%% Plots Histograms

x_ticks = np.arange(-1,1.05,0.1)
simdf = pd.DataFrame(sim, columns = ['word1', 'word2', 'simularity'])
simdf = simdf[simdf['simularity']!=1]
simdf.plot(kind = 'hist', bins = 100, xlim = (-1,1), 
           xticks = x_ticks, figsize = (15,8))
#%%
import csv
headers = ('paper name', 'score')

with open('piescores.csv', 'w', newline = '') as outFile:
    wtr = csv.writer(outFile)
    wtr.writerow(headers)
    wtr.writerows(output)
