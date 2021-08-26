r#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 09:06:43 2019

@author: yeatesd, sabbatim, greenbur
Combination of PDFtoSQLite, TikaTest and DocToken
"""
import tika
tika.initVM()
from tika import parser
import spacy
from collections import defaultdict
import sqlite3
import os
import sys
import SQLite
import PostgreSQL
import re
import json
import psycopg2
import argparse
spacy_nlp = spacy.load('en_core_web_lg')

PDFfolder = 'enter folder containing input pdf files here'
database_location = 'enter output location here'

def readpdflistsentences(filelocation):
    """Module tajes path to text file location and returns a list of sentences from doc using Tika
    Args:
        filelocation: Location of document file
    
    Returns:
        listofsents: list of sentences found in the document
    """
    print("Parsing file with Tika...")
    parsed = parser.from_file(filelocation)
    #print(parsed["metadata"])
    #print(parsed["content"])
    try:
        doctext = parsed["content"].strip().replace("\r","").replace("\n","")

    except:
        print("Document has no text")
        doctext = ''

    listofsents = []

    return listofsents, doctext

def readreadpdftoDocummentTrain(filelocation):
    """Module takes path to text file location and returns a list of sentences from doc using Tike
    Args:
        filelocation: location of the document file

    Returns:
        doctext: text from the document
    """
    print("Parsing file with Tika...")
    parsed = parser.from_file(filelocation)
    try:
        doctext = parsed["content"].strip().replace("\r","").replace("\n","")

    except:
        print("Document has no text")
        doctext = ''
    return doctext

def readpdfRaw(filelocation):
    """Module takes path to text file location and returns a list of sentences from doc using Tika
    Args:
        filelocation: location of the document file

    Returns:
        doctext: text from the document
    """
    print("Parsing file with Tika...")
    parsed = parser.from_file(filelocation)
    try:
        doctext = parsed["content"]
        docmeta = parsed["metadata"]

    except Exception as E:
        print(E, "Document has no text")
        doctext = ''
    return doctext, docmeta


def cleanupdocuments(documents):
    # Tokenize the documents, remove common words as well as words that only appear once.
    # Remove common words and tokenize
    stoplist = spacy.lang.en.stop_words.STOP_WORDS
    
    texts = [
            [word for word in document.lower().replace("-","").split() if word not in stoplist]
            for document in documents
            ]
    
    #remove words that appear only once and have a length more than 1 character
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
            
    texts = [
            [token for token in text if frequency[token] > 1 and len(token) > 1 and "http" not in token]
            for text in texts
            ]
    
    # Remove non alpha characters
    texts = [
            #[''.join(filter(str.isalpha, s)) for s in text]
            [t for t in text if not re.search(r"[^A-Za-z ]+", t)]
            for text in texts
            ]
    
    # Remove empty records
    texts = [
            [s for s in text if len(s) > 1]
            for text in texts
            ]
    return texts
#%%
parse = argparse.ArgumentParser()
# choices limits argument values to the
# given list
parse.add_argument('--db',dest='Database', choices=['SQLite','sqlite','PostgreSQL','postgresql'],
                   help='Pick database between either SQLite or PostgreSQL')

args = parse.parse_args()
fmt = args.Database

if fmt == 'SQLite' or fmt == 'sqlite' or fmt == '':
    #Locations of files
    #TODO: Add for loop make doclocation folder of pdf files
    #Copy database for each project then populate
    converted = 0
    failed = 0
    failed_list = []
    if __name__ == '__main__':

        tablename = 'newpapers'
        SQLite.create_NLP_Table(database_location, tablename)
        #PDFfolder = sys.argv[0]
        #TODO: argparse for this
        list = os.walk(PDFfolder)
        
        total = 0
        for path, dir, filenames in list:
            for filename in filenames:
                if '.pdf' in filename:
                    doc = os.path.join(path,filename)
                    print(doc)
                    total += 1

                    #database_location = sys.argv[2]
                     #get text from pdf
                    try:
                        doctext, metadata = readpdfRaw(doc)
                    
                        #connect to database and print all tables in the database
                        ##this returns the connection (conn) and the cursor (cursor)
                        cursor, conn = SQLite.connect_to_database(database_location)
                        ##this lists all tables in the database and print
                        database_table_list = SQLite.list_tables(cursor)
                        
                        
                        #add row to database
                        ##custom sql code for the papers table in the database
                        sql = ''' INSERT INTO {0}(file_location, raw_document_data, metadata) VALUES(%s,%s,%s) '''.format(tablename)
                        ##create list for data to be appended to database table papers
                    
                   
                        data = [doc, doctext.strip(), json.dumps(metadata)]
                        ##execute insert
                        SQLite.insert_row(conn, cursor, sql, data)
                        converted +=1
                        print('doc converted')

                    except Exception as E: 
                        failed_list.append(doc)
                        failed +=1
                        print(E, 'nope')
                        continue
            

#print(converted/total,'% converted')
   

elif fmt == 'PostgreSQL' or fmt == 'postgresql':
    #Locations of files
    #TODO: Add for loop make doclocation folder of pdf files
    #Copy database for each project then populate
    converted = 0
    failed = 0
    failed_list = []
    tablename = "Sweetness"

    if __name__ == '__main__':
        #PDFfolder = sys.argv[0]
        #TODO: Argparse for this
        newtablename = tablename
        list = os.walk(PDFfolder)
        PostgreSQL.create_NLP_Table(newtablename)


        total = 0
        for path, dir, filenames in list:
            for filename in filenames:
                if '.pdf' in filename:
                    doc = os.path.join(path,filename)
                    print(doc)
                    total += 1              
                     #get text from pdf
                    try:
                        doctext, metadata = readpdfRaw(doc)

                        PostgresConn, PostgresCursor = PostgreSQL.connect_to_database()

                        
                        #add row to database
                        ##custom sql code for the papers table in the database
                        #create list for data to be appended to database table papers
                        postgresSQL = ''' INSERT INTO {0}(file_location, raw_document_data, metadata) VALUES(%s,%s,%s) '''.format(tablename)
 
                   
                        postgresData = (doc, doctext.strip(), json.dumps(metadata))

                        ##execute insert
                        PostgreSQL.insert_row(PostgresConn, PostgresCursor, postgresSQL, postgresData)
          
                        converted +=1
                        print('doc converted')

                            
                        #for row in paperdata:
                           # print(row)
                    except Exception as E: 
                        failed_list.append(doc)
                        failed +=1
                        print(E, 'nope')
                        continue
            

#print(converted/total,'% converted')

#%%       
import csv
headers = ('Failed Paper Name:')

with open('Failed Papers GEOworkspace.csv','w',newline='', encoding="utf-8") as outFile:
    wtr = csv.writer(outFile)
    wtr.writerow([headers])
    for row in failed_list:
        failed_list = [c.strip() for c in row.strip(',').split(',  ')]
        wtr.writerow(failed_list)
