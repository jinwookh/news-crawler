import requests
from bs4 import BeautifulSoup
import urllib.parse
import sqlite3
from datetime import date, timedelta
import sql_handler

CHOSUN_START_QUOTE = "CHOSUN CRAWLING STARTS!"
DONGA_START_QUOTE = "DONGA CRAWLING STARTS!"
KHAN_START_QUOTE = "KHAN CRAWLING STARTS!"
MUNHWA_START_QUOTE = "MUNHWA CRAWLING STARTS!"
KMIB_START_QUOTE = "KMIB CRAWLING STARTS!"

ALREADY_DONE_QUOTE = "Crawling have already done. Let's skip it"
RESPONSE_ERROR_QOUTE = "Error: response error"
DATE_NONE_QUOTE = "Error: cannot crawl date from site"
SS_LIST_ZERO_QUOTE = "Error: number of ss_list_elements are zero"
HEADLINE_ZERO_QUOTE = "Error: number of headline is 0"
SECTION_LIST_ZERO_QUOTE = "Error: number of section_list_element is 0"
SECTION_TXT_ZERO_QUOTE = "Error: number of section_txt_element is 0"
ARTICLE_ZERO_QUOTE = "Error: number of article is 0"
PAPERLIST_ZERO_QUOTE = "Error: number of papaerlist_element is 0"

NAVER_SEARCH_URL = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
CHOSUN_URL = "http://srchdb1.chosun.com/pdf/i_service/index_new.jsp"
DONGA_URL = "http://news.donga.com/Pdf"
KHAN_URL = "http://paoin.khan.co.kr/service/Khan/Default.aspx"
MUNHWA_URL ="http://www.paoin.com/service/Munhwa/Default.aspx"
KMIB_URL = "http://www.paoin.com/service/Kukinews/Default.aspx" 



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
    iframe_element = resource.find(name="iframe")
    if iframe_element == None:
        crawl_result_list.append(DATE_NONE_QUOTE)
        print(DATE_NONE_QUOTE)
        return crawl_result_list
    link_that_has_date = iframe_element.get("src")
    year = link_that_has_date.split("Y=")[1].split("&")[0]
    month = link_that_has_date.split("M=")[1].split("&")[0]
    day = link_that_has_date.split("D=")[1].split("&")[0]
    date_today = int(year+month+day)




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


    if numOfHeadline == 0:
        crawl_result_list.append(HEADLINE_ZERO_QUOTE)
        print(HEADLINE_ZERO_QUOTE)
        return crawl_result_list
    else:
        failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2)
    
    report = {}
    report['date'] = date_today
    report['news'] = 'chosun'
    report['whole'] = numOfHeadline
    report['none'] = numOfNone + numOfWrongMedia
    report['failure'] = failure_percentage

    sql_handler.inserts_news_list('chosun', news_list)
    sql_handler.inserts_report(report)

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
    if a_element == None:
        crawl_result_list.append(DATE_NONE_QUOTE)
        print(DATE_NONE_QUOTE)
        return crawl_result_list
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


def khan():
    """crawls title and link from khan and naver site, and stores (date, page, title, link) into db"""

    crawl_result_list = []
    crawl_result_list.append(KHAN_START_QUOTE)
    print(KHAN_START_QUOTE)


    response = requests.get(KHAN_URL)
    if response.status_code != 200:
        crawl_result_list.append(RESPONSE_ERROR_QUOTE)
        print(RESPONSE_ERROR_QUOTE)
        return crawl_result_list

    resource = BeautifulSoup(response.text, features = "html.parser")
    


    #below code crawls date from khan site
    selected_elements = resource.find_all(name= "option", attrs={"selected":"selected"})
    if len(selected_elements) < 3:
        crawl_result_list.append(DATE_NONE_QUOTE)
        print(DATE_NONE_QUOTE)
        return crawl_result_list
    year = int(selected_elements[0].get("value"))
    month = int(selected_elements[1].get("value"))
    day = int(selected_elements[2].get("value"))
    date_in_class_date = date(year, month, day)
    date_today = int(str(date_in_class_date).replace("-",""))
    


    article_elements = resource.find_all(name="div", attrs={"class":"article"})
    if len(article_elements) == 0:
        crawl_result_list.append(ARTICLE_ZERO_QUOTE)
        print(ARTICLE_ZERO_QUOTE)
        return crawl_result_list

    news_list = []
    numOfWrongMedia = 0
    numOfAd = 0
    numOfPage = 1
    numOfNone = 0
    numOfHeadline = 0
    
    for article_element in article_elements:
        list_elements = article_element.find_all(name = "li")
        for list_element in list_elements:
            news = {}
            
            a_element = list_element.find(name = "a")
            title = a_element.get("title")
            if title == "":
                title = a_element.get_text().strip()
            
            news['title'] = title
            news['page'] = numOfPage
            news['date'] = date_today


            #below code is for handling title with bracket([])
            #since search is not successful with title with bracket,
            #we will try removing bracket from title if title does not contatin
            #'광고'
            if "[" in title and "]" in title:
                inside_bracket = title.split('[',1)[1].split(']')[0]
                if title.split('[')[0] == '' and title.split(']')[1] == '':
                    numOfAd = numOfAd + 1
                    break
                title = title.replace("["+inside_bracket+"]","")

            title_encoded = urllib.parse.quote(title)
            url = NAVER_SEARCH_URL + title_encoded
            response = requests.get(url)
            resource = BeautifulSoup(response.text,features = "html.parser")
            a_element = resource.find(name ="a", attrs ={ "class":"_sp_each_title"})

            if a_element != None:
                link =  a_element.get('href')
                if link.find("khan") == -1:
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


    if numOfHeadline == 0:
        crawl_result_list.append(HEADLINE_ZERO_QUOTE)
        print(HEADLINE_ZERO_QUOTE)
        return crawl_result_list
    else:
        failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2)

    report = {}
    report['date'] = date_today
    report['news'] = 'khan'
    report['whole'] = numOfHeadline
    report['none'] = numOfNone + numOfWrongMedia
    report['failure'] = failure_percentage
    
    sql_handler.inserts_news_list('khan', news_list)
    sql_handler.inserts_report(report)

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


def munhwa(): 
    """crawls news headline from chosun, and link from naver, then adds 
    (date, page, title, link) to the database."""
    crawl_result_list = []
    crawl_result_list.append(MUNHWA_START_QUOTE)
    print(MUNHWA_START_QUOTE)


    response = requests.get(MUNHWA_URL)
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

    paperlist_elements =  resource.find_all(name="div", attrs={"class":"paperlist"})
    if len(paperlist_elements) == 0:
        crawl_result_list.append(PAPERLIST_ZERO_QUOTE)
        print(PAPERLIST_ZERO_QUOTE)
        return crawl_result_list




    #below code crawls date from munhwa  site
    selected_elements = resource.find_all(name= "option", attrs={"selected":"selected"})
    if len(selected_elements) < 3:
        crawl_result_list.append(DATE_NONE_QUOTE)
        print(DATE_NONE_QUOTE)
        return crawl_result_list
    year = int(selected_elements[0].get("value"))
    month = int(selected_elements[1].get("value"))
    day = int(selected_elements[2].get("value"))
    date_in_class_date = date(year, month, day)
    date_today = int(str(date_in_class_date).replace("-",""))




    for paperlist_element in paperlist_elements:
        a_elements = paperlist_element.find_all(name = "a")
        for a_element in a_elements:
            news = {}
            title = a_element.get_text().strip()
            news['title'] = title
            news['page'] = numOfPage
            news['date'] = date_today

            if "[" in title and "]" in title:
                inside_bracket = title.split('[',1)[1].split(']')[0]
                if title.split('[')[0] == '' and title.split(']')[1] == '':
                    numOfAd = numOfAd + 1
                    break
                title = title.replace("["+inside_bracket+"]","")

            title_encoded = urllib.parse.quote(title)
            url = NAVER_SEARCH_URL + title_encoded
            response = requests.get(url)
            resource = BeautifulSoup(response.text,features = "html.parser")
            a_element = resource.find(name ="a", attrs ={ "class":"_sp_each_title"})
            if a_element != None:
                link =  a_element.get('href')
                if link.find("munhwa") == -1:
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


    sql_handler.inserts_news_list('munhwa', news_list)

    if numOfHeadline == 0:
        crawl_result_list.append(HEADLINE_ZERO_QUOTE)
        print(HEADLINE_ZERO_QUOTE)
        return crawl_result_list
    else:
        failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2)

    report = {}
    report['date'] = date_today
    report['news'] = 'munhwa'
    report['whole'] = numOfHeadline
    report['none'] = numOfNone + numOfWrongMedia
    report['failure'] = failure_percentage
    
    sql_handler.inserts_news_list('munhwa', news_list)
    sql_handler.inserts_report(report)

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
