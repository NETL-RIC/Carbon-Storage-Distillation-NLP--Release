#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 09:06:43 2019

@author: sabbatim
These modules are a simplified wrapper for SQLalchemy to connect to PostgreSQL database
"""
# from sqlalchemy import create_engine
import pandas as pd
import psycopg2

# Connection modules


def connect_to_database(databasename='', databaseIP='', databaseport='', username='',
                       password=''):
    """Module takes arguments to connect to a PostgreSQL database using SQL Alchemy and returns a connection.

    Args:
        databasename: Name of the database to connect. Default livingdb
        databaseIP: IP address of the database server.
        databaseport: Port of the database server
        username: DB username
        password: User password

    Returns:
        connection: connection to the database
        cursor: cursor for database connection

    """
    # Create the connection
    connection = psycopg2.connect(host=databaseIP, user=username, password=password, dbname=databasename)
    cursor = connection.cursor()
    return connection, cursor


def disconnect_from_db(dbconnection, cursor):
    #closes connecttion to database
    cursor.close()
    dbconnection.close()


# editing modules

def create_NLP_Table(newtablename):
    #this module will create a table with the given name with the standard fields for nlp
    dbconnection, cursor = connect_to_database()
    create_table(dbconnection, cursor, newtablename)
    add_field(dbconnection, cursor, newtablename, "file_location", "TEXT")
    add_field(dbconnection, cursor, newtablename, "metadata", "TEXT")
    add_field(dbconnection, cursor, newtablename, "title", "TEXT")
    add_field(dbconnection, cursor, newtablename, "source_url", "TEXT")
    add_field(dbconnection, cursor, newtablename, "raw_document_data", "TEXT")
    add_field(dbconnection, cursor, newtablename, "clean_doc_data", "TEXT")
    add_field(dbconnection, cursor, newtablename, "clean_doc_data_2", "TEXT")
    add_field(dbconnection, cursor, newtablename, "classification", "TEXT")
    add_field(dbconnection, cursor, newtablename, "subclassification", "TEXT")
    add_field(dbconnection, cursor, newtablename, "locationlist", "TEXT")
    add_field(dbconnection, cursor, newtablename, "latitude", "TEXT")
    add_field(dbconnection, cursor, newtablename, "longitude", "TEXT")

def create_table(dbconnection, cursor, newtablename):
    """Module take a db connection and table name string and creates a table with minimal fields

    Args:
        dbconnection: A PostgreSQL connection
        cursor: Cursor connection to database
        newtablename: String for a new table name

    Returns:
        none
    """
    #remove adding timestamp 'created_on TIMESTAMP NOT NULL'
    sql = ''' CREATE TABLE %s (oid serial PRIMARY KEY) ''' % newtablename
    cursor.execute(sql)
    dbconnection.commit()


def add_field(dbconnection, cursor, tablename, fieldname='newfield', fieldtype='TEXT'):
    """Module takes db connection, table name and new field information and updates the table with a new field

    Args:
        dbconnection: A PostgreSQL connection
        cursor: Cursor connection to database
        tablename: String for a table name
        fieldname: list of a field name and a data type to add
        fieldtype: type of field to be created default is TEXT

    Returns:
        none
    """
    sql = '''ALTER TABLE {0} ADD COLUMN {1} {2}'''.format(tablename, fieldname, fieldtype)
    cursor.execute(sql)
    dbconnection.commit()

def insert_row(conn2, cursor2, sql, data):
    # takes list of data and table fields and adds new row to database
    #modify the sql statement for other databases this is only for the papers table
    #data = (metadata['title'], doclocation, doctext.strip())
    cursor2.execute(sql, data)
    #cursor.close()
    conn2.commit()

def insert_row_new(conn, cursor, tablename, data, fieldnames=['file_location', 'raw_document_data']):
    """
    This takes connection, table, fields and data anc writes a new row to the database
    TODO: edit to include all data that is generated
    Args:
        conn: connection to the database
        cursor: Cursor connection to the database
        tablename: name of table to be edited
        fieldnames: List of fields to be populated by data
        data: List of data to be added to the fields listed in fieldnames

    Returns:
        none

    """
    if len(data) == len(fieldnames):
        sql = ''' INSERT INTO {0}({1}, {2}) VALUES(%s,%s) '''.format(tablename, fieldnames[0], fieldnames[1])
        # takes list of data and table fields and adds new row to database
        #modify the sql statement for other databases this is only for the papers table
        #data = (metadata['title'], doclocation, doctext.strip())
        cursor.execute(sql, data)
    #cursor.close()
    conn.commit()

def edit_row(conn, cursor, tablename, fieldname, value, idfield, idvalue):
    """

    Args:
        conn: connection to the database
        cursor: Cursor connection to the database
        tablename: name of table to be edited
        fieldname: text name of field to be updated
        value: new field value
        idfield: default should be "oid" unique ID field of the row to be edited
        idvalue: integer record number of row to be edited

    Returns:
        none
    """
    if type(idvalue) is int:
        sql = ''' UPDATE "{0}" SET "{1}" = '{2}' WHERE "{3}" = {4} '''.format(tablename, fieldname, value, idfield,
                                                                              idvalue)
    if type(idvalue) is str:
        sql = ''' UPDATE "{0}" SET "{1}" = '{2}' WHERE "{3}" = '{4}' '''.format(tablename, fieldname, value, idfield,
                                                                              idvalue)
    cursor.execute(sql)
    conn.commit()

# Query Modules


def list_tables(cursor):
    """Module takes a connection to a postgres DB and returns a list of tables in the public schema

    Args:
        dbconnection: A PostgreSQL connection
        cursor: Cursor connection to database

    Returns:
        tablelist: A list of tables in the public schema

    """
    cursor.execute("""SELECT tablename FROM pg_tables WHERE schemaname = 'public'""")
    tablelist = cursor.fetchall()
    return tablelist


def list_fields(cursor, table):
    # list fields in given table
    sql = ''' SELECT * FROM %s ''' % table
    cursor.execute(sql)
    field_names = [description[0] for description in cursor.description]
    return field_names


def list_all_rows(cursor, table):
    #takes connection table and X number of rows and prints X rows in table
    sql = ''' SELECT * from %s''' % table
    #print(cursor.execute(sql))
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


if __name__ == '__main__':

    # this is just test stuff for now
    conn, cur = connect_to_database()

    tablename = "deletenewnlpdata"
    create_NLP_Table(tablename)

    df = list_tables(cur)

    for d in df:
        print(d[0])
    edit_row(conn, cur, tablename, "clean_doc_data", "clean data", "oid", 1)
    #print(list_fields(cur, "papers"))
    # to add data to a table
    #create list for data to be appended to database table papers
    #data = [doc, doctext.strip()]
    #execute insert

    fieldnames = ['id', 'year', 'title', 'event_type', 'pdf_name', 'abstract', 'paper_text']
    testdata = ['this is the document path', 'this is the doc text']
    datafields = ['pdf_name', 'paper_text']

    create_table(conn, cur, "papers")

    for name in fieldnames:
        add_field(conn, cur, "papers", fieldname=name, fieldtype='TEXT')

    insert_row(conn, cur, "papers", testdata, datafields)

    print("done")
    conn.close()



