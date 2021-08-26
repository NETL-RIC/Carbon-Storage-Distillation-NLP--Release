# Carbon-Storage-Distillation-NLP--Release
Source code for Natural Language Processing devolped to work with geological/scientific papers, developed at The National Energy Technology Lab (NETL) in Albany Oregon. Originally developed by David W. (Bart) Yeates, Mike Sabbatino, Samuel Walker, and Randall Greenburg.
Application of code is described in manuscript "Distilling Data to Drive Carbon Storage Insights" by Paige Morkner, Jennifer Bauer, Christopher Creason, Michael Sabbatino, Patrick Wingo1, Randall Greenburg, Samuel Walker, David Yeates, and Kelly Rose.
Contact information: Michael Sabbatino, Michael.Sabbatino@netl.doe.gov, 541-967-5960 (office)

# Instructions
This project contains multiple scripts that are used to process input documents, generate input data for the Gensim library and create an output topic model from the input documents. This readme file will walk through the scripts in the order used for this project.
## PDFtoDatabase.py
This script takes a folder of PDF files as in input parameter and creates a database of all the files in the folder with the text and PDF metadata extracted using the Tika library.  
Before running this script edit the 2 variables PDFfolder and database_location with the path to the folder containing the input documents and a path where you want to save the output SQLite database.
Links to sample input documents are located in the Input Data folder of this repository.
## LDA_optimize_group_number.py
This script takes the output database created in the previous script and cleans up the document text, creates corpus and dictionary for processing in Gensim. The script then uses the Gensim LDA model tools to create multiple LDA models and test each model for coherence value. The output of this script creates multiple LDA modes and a graph of the coherency so that an optimal model can be selected.
Before running this script edit the variable database_location with the path of the SQLite database that you want to process.
## VisualizeNLPModelTopics.py
This script uses the pyLDAvis library to create a visualization of an LDA model. This interactive visualizer provides a dashboard of the model with topic numbers, keywords, and other data that is helpful in analyzing the models.

## AllPaperTopicClass.py
 This is the final python script that takes an input database location and a selected LDA model and outputs a CSV list of all the documents with the papers name and score. This data was combined with the input database to create the spreadsheet located in the results folder of this repository. 

The remaining scripts in this repository are additional tools for analyzing the output of the model or creating visualizations of the output model and data.



