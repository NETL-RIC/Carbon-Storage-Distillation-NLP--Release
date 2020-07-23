# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 10:58:39 2019

@author: yeatesd
"""

import gensim.corpora as corpora
import gensim
import pyLDAvis
import pyLDAvis.gensim
from PDFtoDatabase import cleanupdocuments #custom cleanup module
import SQLite #custom sql query module
import time


start_time = time.time()
print('Time Started')
#user variables
#location of sqlite database
database_location = r"E:\Spyder\NLP\WorkingPapersALL.sqlite"      #Connect to your database
#path where model will be saved
topics= [7,9,11]
for i in topics:
    #generating strings for to save files    
    istr = str(i)
    path = r"E:\Spyder\NLP\ALLvec2viz",istr,".txt"                   #Change model name
    pathstr = ''.join(path)
    visave = 'LDA_nt',istr,'_ALL_AUTO.html'                        #Change File name
    visavestr = ''.join(visave)
    
    
    savemodelpath = path                #Change name of model
    
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
    id2word.save('dictionary.gensim')
    #generate corpus with doc2bow
    corpus = [id2word.doc2bow(text) for text in cleandoc]
    
    #generate LDA model for 10 topics
    print("generating LDA model")
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                               id2word=id2word,
                                               num_topics=i, 
                                               random_state=100,
                                               update_every=1,
                                               chunksize=100,
                                               passes=10,
                                               alpha='auto',
                                               per_word_topics=True)
    
    print("print topics")
    print(lda_model.show_topics())
    lda_model.save(str(i)+'topicLDAModel.gensim')


    #generate Visualiziation
    #pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
    print("Open interactive visualization in web browser")
    pyLDAvis.display(vis)
    pyLDAvis.save_html(vis,visavestr)                                          
print("--- %s seconds ---" % (time.time() - start_time))

   
  