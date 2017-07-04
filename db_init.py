import sqlite3
import settings

SQL_FILE_NAME = settings.SQL_FILE_NAME
DB_NAME = settings.DB_NAME

#Read Table Schema into a Variable and remove all New Line Chars
TableSchema=""
with open(SQL_FILE_NAME, 'r') as SchemaFile:
 TableSchema=SchemaFile.read().replace('\n','').replace('\r','')

#Connect or Create DB File
conn = sqlite3.connect(DB_NAME)
curs = conn.cursor()

#Create Tables
sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

#Close DB
curs.close()
conn.close()