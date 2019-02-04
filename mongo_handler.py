import pymongo
from datetime import date

DB_NAME = "news-db"

date_in_integer = int(str(date.toda()).replace("-",""))

def insert(table_name, news_list):
    if type(news_list) != type([]):
        raise TypeError("list of news hould be list")
    if table_name not in ["chosun", "donga", "khan", "munhwa", "kmib"]:
        raise BaseException("wrong table name")

    client = MongoClient()
    db = client[DB_NAME]
    news_collection = db[table_name]
    
    for news in news_list:
        news_info = { "date": date_in_integer, "page":news['page'], "title":news['title'], "link": news['link'] }
        news_collection.insert_one(news_info)

    client.close()
    

def show_all ( table_name ):
    if table_name not in ["chosun","donga","khan","munhwa","kmib"]:
        raise BaseException("wrong table name")

    client = MongoClient()
    db = client[DB_NAME]
    news_collection = db[table_name]

    for news in news_collection.find():
        print(news)


