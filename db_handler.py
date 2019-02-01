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

def db_insert(table_name, news_list):
    connection = sqlite3.connect('news.db')
    db_cursor = connection.cursor()
    if type(table_name) != str:
        raise TypeError("table name should be string")
    if type(news_list) != type([]):
        raise TypeError("list of news should be list")

    for news in news_list:
        if type(news) != type({}):
            raise TypeError("news in news_list should be dictionary type")
        db_cursor.execute("INSERT INTO ? VALUES (?,?,?,?)",tablbe_name, news['page'],news['title'], news['link'])


