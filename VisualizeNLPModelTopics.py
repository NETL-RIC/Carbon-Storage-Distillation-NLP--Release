# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 15:21:22 2019

@author: sabbatim
"""

#import modules
import gensim.corpora as corpora
import gensim
import pyLDAvis
import pyLDAvis.gensim
from PDFtoDatabase import cleanupdocuments #custom cleanup module
import SQLite #custom sql query module
import sys
#user variables
#location of sqlite database
database_location = r"E:\NATCARB\NATCARBCleanuptool\Test_Training_Data\WorkingPapersNATCARB.sqlite"
# =============================================================================
# Using sys.argv requires the user to make a command line argument so if this
# is being run from an IDE then you'll want to use the above line to get to 
# your database. If used from the command line you need to add your path to the
# database. To run from a UNIX command line us the line below, make sure to 
# change your path. 
# python VisualizeNLPModelTopcs.py '/home/greenbur/NLP/Python Code/WorkingPapersCS.sqlite'
# Same thing goes for the savemodelpath below. This will add another argument 
# to your command line. So you will run the below command, keep in mind the path
# needs to be changed:
# python VisualizeNLPModelTopcs.py '/home/greenbur/NLP/Python Code/WorkingPapersCS.sqlite' '/home/greenbur/NLP/Results/GOMXlgvec.txt'
# The above command is all one line. 
# =============================================================================
#database_location = sys.argv[1]

#path where model will be saved
savemodelpath = r"E:\NATCARB\NATCARBCleanuptool\Test_Training_Data\NATCARBvec2.txt"
#savemodelpath = sys.argv[2]

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


print("Documents loaded and ready to process")
#Generate dictionary      
id2word = corpora.Dictionary(cleandoc)
#generate corpus with doc2bow
corpus = [id2word.doc2bow(text) for text in cleandoc]

#generate LDA model for 10 topics
print("generating LDA model")
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=10, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)

print("print topics")
print(lda_model.show_topics())

#generate Visualiziation
vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
print("Open interactive visualization in web browser")
pyLDAvis.show(vis)
