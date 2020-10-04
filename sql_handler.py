import sqlite3

news_site_list = ['chosun', 'kmib','khan', 'donga', 'munhwa', 'seoul', 'mk']
table_list = news_site_list + ['crawling_result'] 

connection = sqlite3.connect('news.db')
db_cursor = connection.cursor()

db_cursor.execute("CREATE TABLE IF NOT EXISTS chosun (date INTEGER, page INTEGER, title TEXT, link TEXT)")
db_cursor.execute("CREATE TABLE IF NOT EXISTS donga (date INTEGER, page INTEGER, title TEXT, link TEXT)")
db_cursor.execute("CREATE TABLE IF NOT EXISTS khan (date INTEGER, page INTEGER, title TEXT, link TEXT)")
db_cursor.execute("CREATE TABLE IF NOT EXISTS munhwa (date INTEGER, page INTEGER, title TEXT, link TEXT)")
db_cursor.execute("CREATE TABLE IF NOT EXISTS kmib (date INTEGER, page INTEGER, title TEXT, link TEXT)")
db_cursor.execute("CREATE TABLE IF NOT EXISTS seoul (date INTEGER, page INTEGER, title TEXT, link TEXT)")
db_cursor.execute("CREATE TABLE IF NOT EXISTS mk (date INTEGER, page INTEGER, title TEXT, link TEXT)")

db_cursor.execute("CREATE TABLE IF NOT EXISTS crawling_result (date INTEGER, news TEXT, whole INTEGER, none INTEGER, failure REAL)")

db_cursor.close()
connection.close()

def inserts_news_list(table_name, news_list):
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
        db_parameter_list.append(news['date'])
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
  
def inserts_report(report):
    connection = sqlite3.connect('news.db')
    db_cursor = connection.cursor()
    table_name = "crawling_result"

    if type(report) != type({}):
        raise TypeError("report should be dictionary")

    db_parameter_list = []
    db_parameter_list.append(report['date'])
    db_parameter_list.append(report['news'])
    db_parameter_list.append(report['whole'])
    db_parameter_list.append(report['none'])
    db_parameter_list.append(report['failure'])
        
    check_repetition_query = "select * from " +table_name + " where date=? and news=?"
    date = report['date']
    news_company_name = report['news']
    tuplified_conditions = (date, news_company_name )
    repetition_result = db_cursor.execute( check_repetition_query, tuplified_conditions).fetchone()  

    if repetition_result == None:
        insert_query = "INSERT INTO " + table_name + " VALUES(?,?,?,?,?)"
        db_cursor.execute( insert_query, db_parameter_list)

    connection.commit()
    connection.close()


def already_crawled(table_name, date_today):
    
    """DEPRECATED"""

    if table_name not in news_site_list:
        raise BaseException("Error: site name is not included in list")

    connection = sqlite3.connect('news.db')
    db_cursor = connection.cursor()
    query = "select * from " +table_name + " where date=?"
    tuplified_date_today = (date_today, )
    repetition_result = db_cursor.execute( query, tuplified_date_today).fetchone()
    if repetition_result == None:
        result =  False
    else:
        result =  True

    connection.close()
    return result

def shows_all( table_name ):
    if table_name not in table_list:
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

    """DEPRECATED"""

    f = open("news-db.txt","w")
    connection = sqlite3.connect('news.db')
    db_cursor = connection.cursor()
    for table_name in news_site_list:
        f.write("\n" + table_name + "\n")
        query = "select * from " + table_name
        rows =db_cursor.execute(query)
        for row in rows:
            f.write(str(row)+"\n")
    f.close()
    
    table_name = "crawling_result"
    f = open("report-db.txt", "w")
    f.write("\n" + table_name + "\n")
    query = "select * from " + table_name
    rows =db_cursor.execute(query)
    for row in rows:
        f.write(str(row)+"\n")
    f.close()
    connection.close()
    
