# -*- coding: utf-8 -*-
"""
Created on Fri September 12th 11:27:17 2019

@author: greenbur
"""
import gensim.corpora as corpora
from PDFtoDatabase import cleanupdocuments #custom cleanup module
import SQLite #custom sql query module
from gensim.models import TfidfModel
from gensim.corpora import Dictionary
import pickle
import sys

#Load documents from database
database_location = sys.argv[1]
# database_location = '/home/greenbur/NLP/Databases/eXtremeMAT_Maddison.sqlite'

def stopwords():
    cursor, conn = SQLite.connect_to_databse(database_location)
    datatable = SQLite.list_all_rows(cursor, 'papers')
    paperdata = []
    for row in datatable:
        paperdata.append(row[6])

    cleandoc = cleanupdocuments(paperdata)
    id2word = corpora.Dictionary(cleandoc)
    corpus = [id2word.doc2bow(text) for text in cleandoc]
    dictionary = corpora.Dictionary(cleandoc)

    pickle.dump(corpus, open('ALL_corpus.pkl', 'wb'))
    dictionary.save('ALL_dictionary.gensim')

    cp_all = []
    for i in range (0,len(cleandoc)):
        for j in range (0,len(cleandoc[i])):
            cp_all.append(cleandoc[i][j])

    cleandoc.insert(0,cp_all)
    print('done part dos, **thumbs up**')

    dct = Dictionary.load('ALL_dictionary.gensim')
    corpus = [dct.doc2bow(line) for line in cleandoc]
    model = TfidfModel(corpus)
    vector = model[corpus[0]]
    print('done part tres, **smiley face**')

    cp_stop = []
    for token_id, token_weight in vector:
        cp_stop.append((dct.get(token_id),token_weight))
    print('done part quatros, yeehaw!')

    import csv
    headers = ('word','score')

    with open('stopwords.csv','w',newline='',encoding='utf-8') as outFile:
        wtr = csv.writer(outFile)
        wtr.writerow(headers)
        wtr.writerows(cp_stop)

    with open('stopwords.csv', 'r', newline='', encoding='utf-8') as inFile:
        csvreader = csv.reader(inFile)
        itr = iter(csvreader)
        next(itr)
        # stopwordvalue = [row for row in itr if float(row[1]) > 0.007]
        stopwordvalue = [row for row in itr if float(row[1]) > float(sys.argv[2])]

    with open('stopwords.csv','w',newline='',encoding='utf-8') as OutFile:
        wt = csv.writer(OutFile)
        wt.writerow(headers)
        wt.writerows(stopwordvalue)

    print('STOP WORDS FOUND!!! Stored in stopwords.csv')
stopwords()
