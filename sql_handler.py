import sqlite3
from datetime import date

date_in_integer = int(str(date.today()).replace("-",""))
news_site_list = ['chosun', 'kmib','khan', 'donga', 'munhwa']  

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
    assert(table_name in news_site_list, "wrong table name" )

    for news in news_list:
        if type(news) != type({}):
            raise TypeError("news in news_list should be dictionary type")
        db_parameter_list = []
        db_parameter_list.append(date_in_integer)
        db_parameter_list.append(news['page'])
        db_parameter_list.append(news['title'])
        db_parameter_list.append(news['link'])
        
        insert_query = "INSERT INTO " + table_name + " VALUES(?,?,?,?)"


        check_repetition_query = "select * from " +table_name + " where title=?"
        title = news['title']
        tuplified_title = (title, )
        repetition_result = db_cursor.execute( check_repetition_query, tuplified_title).fetchone()

        if repetition_result == None:
            insert_query = "INSERT INTO " + table_name + " VALUES(?,?,?,?)"
            db_cursor.execute( insert_query, db_parameter_list)

    connection.commit()    
    connection.close()
    
def shows_all( table_name ):
    if table_name not in news_site_list:
        raise BaseException("Error: site name is not included in list")

    connection = sqlite3.connect('news.db')
    db_cursor = connection.cursor()
    query = "select * from " + table_name
    
    rows = db_cursor.execute(query)
    for row in rows:
        print(type(row))
        print(row)
    connection.close()

def converts_db_into_text_file():
    f = open("news-db.txt","w")
    connection = sqlite3.connect('news.db')
    db_cursor = connection.cursor()
    for table_name in news_site_list:
        f.write("\n" + table_name + "\n")
        query = "select * from " + table_name
        rows =db_cursor.execute(query)
        for row in rows:
            f.write(str(row)+"\n")
    
    connection.close()
    f.close()
