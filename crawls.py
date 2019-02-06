import requests
from bs4 import BeautifulSoup
import urllib.parse
import sqlite3
from datetime import date, timedelta
import sql_handler

CHOSUN_START_QUOTE = "CHOSUN CRAWLING STARTS!"
DONGA_START_QUOTE = "DONGA CRAWLING STARTS!"

RESPONSE_ERROR_QOUTE = "Error: response error"
DATE_NONE_QUOTE = "Error: cannot crawl date from site"
SS_LIST_ZERO_QUOTE = "Error: number of ss_list_elements are zero"
HEADLINE_ZERO_QUOTE = "Error: number of headline is 0"
SECTION_LIST_ZERO_QUOTE = "Error: number of section_list_element is 0"
SECTION_TXT_ZERO_QUOTE = "Error: number of section_txt_element is 0"




NAVER_SEARCH_URL = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
CHOSUN_URL = "http://srchdb1.chosun.com/pdf/i_service/index_new.jsp?Y=2019&M=02&D=01"
DONGA_URL = "http://news.donga.com/Pdf?ymd=20190202"



def chosun(): 
    """crawls news headline from chosun, and link from naver, then adds 
    (date, page, title, link) to the database."""
    crawl_result_list = []
    crawl_result_list.append(CHOSUN_START_QUOTE)
    print(CHOSUN_START_QUOTE)

    response = requests.get(CHOSUN_URL)
    if response.status_code != 200:
        crawl_result_list.append(RESPONSE_ERROR_QUOTE)
        print(RESPONSE_ERROR_QUOTE)
        return crawl_result_list

    news_list = []
    numOfWrongMedia = 0
    numOfAd = 0
    numOfPage = 1
    numOfNone = 0
    numOfHeadline = 0

    resource = BeautifulSoup(response.text,features = "html.parser")

    ss_list_elements =  resource.find_all(name="div", attrs={"class":"ss_list"})
    if len(ss_list_elements) == 0:
        crawl_result_list.append(SS_LIST_ZERO_QUOTE)
        print(SS_LIST_ZERO_QUOTE)
        return crawl_result_list



    #below code crawls date from chosun site
    date_txt_element = resource.find(name="span", attrs={"class":"date_txt"})
    if date_txt_element == None:
        crawl_result_list.append(DATE_NONE_QUOTE)
        print(DATE_NONE_QUOTE)
        return crawl_result_list
    date_txt = date_txt_element.get_text()
    year, month = date_txt.split("년")[0], date_txt.split("년")[1]
    day = month.split("월")[1]
    day = day.split("일")[0]
    month = monoth.split("월")[0]
    day = int(day.strip())
    month = int(month.strip())
    year = int(year.strip())
    date_in_class_date = date(day, month, year)
    date_today = int(str(date_in_class_date).replace("-",""))
    

    for ss_list_element in ss_list_elements:
        li_elements = ss_list_element.find_all(name = "li")
        for li_element in li_elements:
            news = {}
            title = li_element.get_text()
            news['title'] = title
            news['page'] = numOfPage
            news['date'] = date_today
            #below code is for handling title with bracket([])
            #since search is not successful with title with bracket,
            #we will try removing bracket from title if title does not contatin
            #'전면광고'

            if "[" in title and "]" in title:
                inside_bracket = title.split('[',1)[1].split(']')[0]
                if title.find('전면광고') != -1:
                    numOfAd = numOfAd + 1
                    news['link'] = None
                    break
                title = title.replace("["+inside_bracket+"]","")


            title_encoded = urllib.parse.quote(title)
            url = NAVER_SEARCH_URL + title_encoded
            response = requests.get(url)
            resource = BeautifulSoup(response.text,features = "html.parser")
            a_element = resource.find(name ="a", attrs ={ "class":"_sp_each_title"})

            if a_element != None:
                link =  a_element.get('href')
                if link.find("chosun") == -1:
                    numOfWrongMedia = numOfWrongMedia + 1
                    news['link'] = None
                else:
                    news['link'] = link    
            else:
                news['link'] = None
                numOfNone = numOfNone + 1
            
            news_list.append(news)
            numOfHeadline = numOfHeadline + 1
    

        numOfPage = numOfPage + 1


    sql_handler.inserts_news_list('chosun', news_list)

    if numOfHeadline == 0:
        crawl_result_list.append(HEADLINE_ZERO_QUOTE)
        print(HEADLINE_ZERO_QUOTE)
        return crawl_result_list
    else:
        failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2)

    success_quotes = []
    success_quotes.append("number of none: " + str(numOfNone))
    success_quotes.append("number of msmatched news: " + str(numOfWrongMedia))
    success_quotes.append("number of ads: " + str(numOfAd))
    success_quotes.append("number of headline: " + str(numOfHeadline))
    success_quotes.append("failure percentage: " + str(failure_percentage) + "%")
    
    crawl_result_list.extend(success_quotes)
    for success_quote in success_quotes:
        print(success_quote)
    return crawl_result_list


def donga():
    """crawls news headline from donga, and link from naver, then adds 
    (date, page, title, link) to the database."""
    crawl_result_list = []
    crawl_result_list.append(DONGA_START_QUOTE)
    print(DONGA_START_QUOTE)

    response = requests.get(DONGA_URL)
    if response.status_code != 200:
        crawl_result_list.append(RESPONSE_ERROR_QUOTE)
        print(RESPONSE_ERROR_QUOTE)
        return crawl_result_list
    
    resource = BeautifulSoup(response.text, features = "html.parser")



    #crawls date from donga site
    a_element = resource.find(name = "a", attrs={"class":"prev"})
    a_href = a_element.get("href")
    date_yesterday = a_href.split("ymd=")[1]
    year = int(date_yesterday[0:4])
    month = int(date_yesterday[4:6])
    day = int(date_yesterday[6:8])
    date_yesterday = date(year, month, day)
    date_in_class_date = date_yesterday + timedelta(days=1)
    date_today = int(str(date_in_class_date).replace("-",""))



    section_list_element = resource.find(name = "ul", attrs={"class":"section_list"})   
    if section_list_element == None:
        crawl_result_list.append(SECTION_LIST_ZERO_QUOTE)
        print(SECTION_LIST_ZERO_QUOTE)
        return crawl_result_list

    section_txt_elements =  section_list_element.find_all(name="div", attrs={"class":"section_txt"})
    
    if len(section_txt_elements) == 0:
        crawl_result_list.append(SECTION_TXT_ZERO_QUOTE)
        print(SECTION_TXT_ZERO_QUOTE)
        return crawl_result_list
    
    news_list = []
    numOfPage = 1
    numOfNone = 0
    numOfHeadline = 0
    numOfAd = 0
    for section_txt_element in section_txt_elements:
        li_elements = section_txt_element.find_all(name = "li")
        tit_element = section_txt_element.find(name = "span")
        for li_element in li_elements:
            news = {}
            title = li_element.get_text()
            news['date'] = date_today
            news['title'] = title
            news['page'] = numOfPage

            a_element = li_element.find(name="a")
            if a_element == None:
                numOfAd += 1
                break
            else:
                link = a_element.get('href')
                news['link'] = link
            
            news_list.append(news)
            numOfHeadline += 1
       
        numOfPage += 1

    sql_handler.inserts_news_list('donga', news_list)

    success_quotes = []
    success_quotes.append("number of headline: " + str(numOfHeadline))
    success_quotes.append("number of ad: " + str(numOfAd))

    crawl_result_list.extend(success_quotes)
    for success_quote in success_quotes:
        print(success_quote)
    return crawl_result_list
