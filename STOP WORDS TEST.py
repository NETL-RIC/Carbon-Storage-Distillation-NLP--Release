1# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 15:27:17 2019

@author: YeatesD
"""
from gensim.test.utils import common_texts
import gensim.corpora as corpora
from gensim.models import Word2Vec
from PDFtoDatabase import cleanupdocuments #custom cleanup module
import SQLite #custom sql query module
import gzip
import gensim.downloader as api
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
import time
import pickle
import sys
#%%
#database_location = '/home/greenbur/NLP/Databases/XMATCorpus.sqlite'
database_location = sys.argv[1]
#load document data from database

#connect to sqlite database and load data
cursor, conn = SQLite.connect_to_databse(database_location)
datatable = SQLite.list_all_rows(cursor, 'papers')
#collect paper text and load to python list
paperdata = []
for row in datatable:
    paperdata.append(row[6])
#clean text for word to vec processing
cleandoc = cleanupdocuments(paperdata)
#%%
id2word = corpora.Dictionary(cleandoc)
corpus = [id2word.doc2bow(text) for text in cleandoc]
dictionary = corpora.Dictionary(cleandoc)                           

pickle.dump(corpus, open('ALL_corpus.pkl', 'wb'))
dictionary.save('ALL_dictionary.gensim')     
#%%
cp_all = []
for i in range (0,len(cleandoc)):
    for j in range (0,len(cleandoc[i])):
        cp_all.append(cleandoc[i][j])

cleandoc.insert(0,cp_all)        
print('done part 2')
           #%%
dct = Dictionary.load('ALL_dictionary.gensim')
corpus = [dct.doc2bow(line) for line in cleandoc ]  # convert corpus to BoW format
model = TfidfModel(corpus)  # fit model
vector = model[corpus[0]]   # apply model to the first corpus document
print('done part 3')
 #%%   
    
cp_stop = []
for token_id,token_weight in vector:  
    cp_stop.append((dct.get(token_id),token_weight))
print('done part 4')   
#%%
import csv
headers = ('word','score')

#This seems to only work in this order if you have a csv in your Python Code folder
#named ALL_stopwords.csv

#This opens a csv and prints all the stop words in there
with open('ALL_stopwords.csv','w',newline='',encoding="utf-8") as outFile:
    wtr = csv.writer(outFile)
    wtr.writerow(headers)
    wtr.writerows(cp_stop)
    #wtr.writerows(stopwordvalue)

#This takes the stop words and removes the ones above/below a certain score
with open('ALL_stopwords.csv','r',newline='',encoding='utf-8') as inFile:
    csvreader = csv.reader(inFile)
    itr = iter(csvreader)
    next(itr)
    #stopwordvalue = [row for row in itr if float(row[1]) < 0.0007]
    stopwordvalue = [row for row in itr if float(row[1]) > float(sys.argv[2])]
    
#This writes the words above/below the chosen score
with open('ALL_stopwords.csv', 'w',newline='',encoding='utf-8') as OutFile:
    wt = csv.writer(OutFile)
    wt.writerow(headers)
    wt.writerows(stopwordvalue)




#%%
print('STOP WORDS FOUND!!! Stored in ALL_stopwords.csv')       
