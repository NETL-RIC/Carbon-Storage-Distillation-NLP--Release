# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:17:20 2019

@author: yeatesd
"""
import gensim.corpora as corpora
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel
import gensim
import pyLDAvis
import pyLDAvis.gensim
from PDFtoDatabase import cleanupdocuments #custom cleanup module
import SQLite #custom sql query module
import time
import matplotlib.pyplot as plt
#location of sqlite database
database_location = r"E:\Spyder\NLP\WorkingPapersALL.sqlite"      #Connect to your database

#%%
def compute_coherence_values(dictionary, corpus, texts, limit, start, step):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for i in range(start, limit, step):
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=i, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)
        model_list.append(lda_model)
        coherencemodel = CoherenceModel(model=lda_model, texts=cleandoc, dictionary=id2word, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
        print(coherencemodel.get_coherence(),':',i, 'out of 20')

    return model_list, coherence_values
#%%
#location of sqlite database
database_location = r"E:\Spyder\NLP\WorkingPapersALL.sqlite"      #Connect to your database
#path where model will be saved
#savemodelpath = r"E:\Spyder\NLP\750vec2viz5.txt"                 #Change name of model

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
#%%
start_time = time.time() 
model_list, coherence_values = compute_coherence_values(dictionary=id2word, corpus=corpus, texts=cleandoc, start=2, limit=41, step=1)
print("--- %s seconds ---" % (time.time() - start_time))
#%%
# Show graph
limit=41; start=2; step=1;
x = range(start, limit, step)
plt.plot(x, coherence_values)

plt.xlabel("Num Topics")
plt.ylabel("Coherence score")
plt.legend(("coherence_values"), loc='best')
plt.show()


