import sqlite3
#connect to sqlite db
#conn = sqlite3.connect(r'E:\_NLP\NIPS Papers DB\WorkingPapersDB.sqlite')
#c = conn.cursor()

# Connection modules

def connect_to_database(pathtodb):
    #this take a path to an sqlite db and connects to it and creates a cursor
    co = sqlite3.connect(pathtodb)
    c = co.cursor()
    print("Connected to Database")
    return c, co

def disconnect_from_db(conn, cursor):
    #closes connecttion to database
    cursor.close()
    conn.close()

# editing modules

def create_NLP_Table(dbpath, newtablename):
    #this module will create a table with the given name with the standard fields for nlp
    dbconnection, cursor = connect_to_database(dbpath)
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
    sql = ''' CREATE TABLE IF NOT EXISTS %s (oid INTEGER NOT NULL PRIMARY KEY) ''' % newtablename
    cursor.execute(sql)
    #dbconnection.commit()


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
    #dbconnection.commit()

def insert_row(conn, cursor, sql, data):
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

def delete_all_rows_in_table(conn, cursor, table):
    #this will delete all rows in the table
    sql = ''' DELETE FROM %s ''' % table
    cursor.execute(sql)
    conn.commit()

def delete_table(conn, cursor, table):
    # this will the table
    sql = ''' DROP TABLE IF EXISTS %s ''' % table
    cursor.execute(sql)
    conn.commit()

# Query Modules

def list_tables(cursor):
    #lists all tables in a sqlite database
    cursor.execute("select name from sqlite_master where type = 'table';")
    table_list = cursor.fetchall()
    return table_list

def list_fields(cursor, table):
    #list fields in given table
    sql = ''' SELECT * FROM %s ''' % table
    cursor.execute(sql)
    field_names = [description[0] for description in cursor.description]
    return field_names

def list_first_rows(cursor, table, numberofrows=10):
    #takes connection table and X number of rows and prints X rows in table
    sql = ''' SELECT * from %s LIMIT %s''' % (table, numberofrows)
    #print(cursor.execute(sql))
    data = cursor.execute(sql)
    return data

def list_all_rows(cursor, table):
    #takes connection table and X number of rows and prints X rows in table
    sql = ''' SELECT * from %s''' % (table)
    #print(cursor.execute(sql))
    data = cursor.execute(sql)
    return data

# read this https://www.dataquest.io/blog/python-pandas-databases/
# search creating tables with pandas
if __name__ == '__main__':
    database_path = r'E:\_NLP\NIPS Papers DB\TestEmptyDB.sqlite'
    cursor, conn = connect_to_database(database_path)
    tables = list_tables(cursor)
    print(tables)
    listoffields = list_fields(cursor, 'papers')
    print(listoffields)

    #sql to add data to the papers table
    #sql = ''' INSERT INTO papers(title, pdf_name, paper_text) VALUES(?,?,?) '''
    #sample data to add to new row
    data = [1,2,3]
    #insert_row(conn, cursor, sql, data)


    print("Pause")