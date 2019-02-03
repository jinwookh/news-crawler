import sqlite3
from datetime import date

date_in_integer = int(str(date.today()).replace("-",""))

connection = sqlite3.connect('news.db')
db_cursor = connection.cursor()

db_cursor.execute("CREATE TABLE IF NOT EXISTS chosun (date INTEGER, page INTEGER, title TEXT, link TEXT)")
db_cursor.execute("CREATE TABLE IF NOT EXISTS donga (date INTEGER, page INTEGER, title TEXT, link TEXT)")
db_cursor.execute("CREATE TABLE IF NOT EXISTS khan (date INTEGER, page INTEGER, title TEXT, link TEXT)")
db_cursor.execute("CREATE TABLE IF NOT EXISTS munhwa (date INTEGER, page INTEGER, title TEXT, link TEXT)")
db_cursor.execute("CREATE TABLE IF NOT EXISTS kmib (date INTEGER, page INTEGER, title TEXT, link TEXT)")
db_cursor.close()
connection.close()

def insert(table_name, news_list):
    connection = sqlite3.connect('news.db')
    db_cursor = connection.cursor()

    if type(table_name) != str:
        raise TypeError("table name should be string")
    if type(news_list) != type([]):
        raise TypeError("list of news should be list")
    assert(table_name in ["chosun", "donga", "khan", "kmib", "munhwa"], "wrong table name" )

    for news in news_list:
        if type(news) != type({}):
            raise TypeError("news in news_list should be dictionary type")
        db_parameter_list = []
        db_parameter_list.append(date_in_integer)
        db_parameter_list.append(news['page'])
        db_parameter_list.append(news['title'])
        db_parameter_list.append(news['link'])

        query = "INSERT INTO " + table_name + " VALUES(?,?,?,?)"
        db_cursor.execute( query, db_parameter_list)
    connection.commit()    
    connection.close()
    
