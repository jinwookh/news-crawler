import requests
from bs4 import BeautifulSoup
import urllib.parse
import sqlite3
import sql_handler
from datetime import date as Date, timedelta
import re

ALREADY_DONE_QUOTE = "Crawling have already done. Let's skip it"
RESPONSE_ERROR_QUOTE = "Error: response error"
DATE_NONE_QUOTE = "Error: cannot crawl date from site"
SS_LIST_ZERO_QUOTE = "Error: number of ss_list_elements are zero"
HEADLINE_ZERO_QUOTE = "Error: number of headline is 0"
SECTION_LIST_ZERO_QUOTE = "Error: number of section_list_element is 0"
SECTION_TXT_ZERO_QUOTE = "Error: number of section_txt_element is 0"
ARTICLE_ZERO_QUOTE = "Error: number of article is 0"
PAPERLIST_ZERO_QUOTE = "Error: number of papaerlist_element is 0"
A_ZERO_QUOTE = "Error: number of a_element is 0"
PAGE_ZERO_QUOTE = "Error: number of pages are zero"


NAVER_SEARCH_URL = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
CHOSUN_URL = "http://srchdb1.chosun.com/pdf/i_service/index_new.jsp"
DONGA_URL = "http://news.donga.com/Pdf"
KHAN_URL = "http://paoin.khan.co.kr/service/Khan/Default.aspx"
MUNHWA_URL ="http://www.paoin.com/service/Munhwa/Default.aspx"
KMIB_URL = "http://www.paoin.com/service/Kukinews/Default.aspx"
SEOUL_URL = "http://www.paoin.com/service/SeoulEconomic/Default.aspx"
HANKOOK_URL = "http://www.paoin.com/Service/Hankooki2018/Default.aspx"        
MK_URL = "http://epaper.mk.co.kr/PaperList.aspx"

def chosun(date): 
    """crawls news headline from chosun, and link from naver, then adds 
    (company_name, date, page, title, link) to the database."""
    crawl_result_list = []
    
    
    date = date.replace("-","")
    year =  date[0:4]
    month = date[4:6]
    day = date[6:8]
    
    chosun_url = CHOSUN_URL + "?Y=" + year + "&M=" + month + "&D=" + day
    date = int(date)


    response = requests.get(chosun_url)
    if response.status_code != 200:
        crawl_result_list.append(RESPONSE_ERROR_QUOTE)
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
        return crawl_result_list




    #below code extracts title and link
    for ss_list_element in ss_list_elements:
        li_elements = ss_list_element.find_all(name = "li")
        for li_element in li_elements:
            news = {}
            title = li_element.get_text()
            news['company_name'] = 'chosun'
            news['title'] = title
            news['page'] = numOfPage
            news['date'] = date


            #below code is for handling title with bracket([])
            #since search is not successful with title with bracket,
            #we will try removing bracket from title if title does not contatin
            #'전면광고'
            if "[" in title and "]" in title:
                inside_bracket = title.split('[',1)[1].split(']')[0]
                if title.find('전면광고') != -1:
                    numOfAd = numOfAd + 1
                    news['link'] = None
                    continue
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
        return crawl_result_list
    else:
        failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2)
    
    report = {}
    report['date'] = date
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
    return crawl_result_list


def donga(date):
    """crawls news headline from donga, and link from naver, then adds 
    (company_name, date, page, title, link) to the database."""
    crawl_result_list = []

    date = date.replace("-", "")
    donga_url = DONGA_URL + "?ymd=" + date
    date = int(date)

    response = requests.get(donga_url)
    if response.status_code != 200:
        crawl_result_list.append(RESPONSE_ERROR_QUOTE)
        return crawl_result_list
    
    resource = BeautifulSoup(response.text, features = "html.parser")


    section_list_element = resource.find(name = "ul", attrs={"class":"section_list"})   
    if section_list_element == None:
        crawl_result_list.append(SECTION_LIST_ZERO_QUOTE)
        return crawl_result_list

    section_txt_elements =  section_list_element.find_all(name="div", attrs={"class":"section_txt"})
    
    if len(section_txt_elements) == 0:
        crawl_result_list.append(SECTION_TXT_ZERO_QUOTE)
        return crawl_result_list
    
    news_list = []
    numOfNone = 0
    numOfHeadline = 0
    numOfAd = 0
    for section_txt_element in section_txt_elements:
        li_elements = section_txt_element.find_all(name = "li")
        tit_element = section_txt_element.find(name = "span")
        
        page = tit_element.get_text()
        match_object = re.search("\d+", page)
        if match_object == None:
            crawl_result_list.append(PAGE_ZERO_QUOTE)
            return crawl_result_list

        page = int(match_object.group())

        for li_element in li_elements:
            news = {}
            title = li_element.get_text()
            news['company_name'] = 'donga'
            news['date'] = date
            news['title'] = title
            news['page'] = page
            


            a_element = li_element.find(name="a")
            if a_element == None:
                numOfAd += 1
                continue
            else:
                link = a_element.get('href')
                news['link'] = link
            

            news_list.append(news)
            numOfHeadline += 1
       

    sql_handler.inserts_news_list('donga', news_list)
    

    success_quotes = []
    success_quotes.append("number of headline: " + str(numOfHeadline))
    success_quotes.append("number of ad: " + str(numOfAd))

    crawl_result_list.extend(success_quotes)
    return crawl_result_list


def khan(date):
    """crawls title and link from khan and naver site, and stores (company_name,date, page, title, link) into db"""

    crawl_result_list = []
    
    khan_url = KHAN_URL + "?PaperDate=" + date
    date = int(date.replace("-",""))

    response = requests.get(khan_url)
    if response.status_code != 200:
        crawl_result_list.append(RESPONSE_ERROR_QUOTE)
        return crawl_result_list

    resource = BeautifulSoup(response.text, features = "html.parser")
    



    article_elements = resource.find_all(name="div", attrs={"class":"article"})
    if len(article_elements) == 0:
        crawl_result_list.append(ARTICLE_ZERO_QUOTE)
        return crawl_result_list

    news_list = []
    numOfWrongMedia = 0
    numOfAd = 0
    numOfNone = 0
    numOfHeadline = 0
    
    for article_element in article_elements:
        h2_element = article_element.find(name = "h2")
        page = h2_element.get_text()
        match_object = re.search('\d+', page)
        if match_object == None:
            crawl_result_list.append(PAGE_ZERO_QUOTE)
            return crawl_result_list

        page = int(match_object.group())
        
        list_elements = article_element.find_all(name = "li")
        for list_element in list_elements:
            news = {}
            news['company_name'] = 'khan'
            
            a_element = list_element.find(name = "a")
            title = a_element.get("title")
            if title == "":
                title = a_element.get_text().strip()
            
            news['title'] = title
            news['page'] = page
            news['date'] = date
            

            #below code is for handling title with bracket([])
            #since search is not successful with title with bracket,
            #we will try removing bracket from title if title does not contatin
            #'광고'
            if "[" in title and "]" in title:
                inside_bracket = title.split('[',1)[1].split(']')[0]
                if title.split('[')[0] == '' and title.split(']')[1] == '':
                    numOfAd = numOfAd + 1
                    continue
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
    


    if numOfHeadline == 0:
        crawl_result_list.append(HEADLINE_ZERO_QUOTE)
        return crawl_result_list
    else:
        failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2)

    report = {}
    report['date'] = date
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
    return crawl_result_list


def munhwa(date): 
    """crawls news headline from munhwa, and link from naver, then adds 
    (company_name, date, page, title, link) to the database."""
    crawl_result_list = []
   
    munhwa_url = MUNHWA_URL + "?PaperDate=" + date
    date = int(date.replace("-",""))

    response = requests.get(munhwa_url)
    if response.status_code != 200:
        crawl_result_list.append(RESPONSE_ERROR_QUOTE)
        return crawl_result_list

    news_list = []
    numOfWrongMedia = 0
    numOfAd = 0
    numOfNone = 0
    numOfHeadline = 0

    resource = BeautifulSoup(response.text,features = "html.parser")


    paperlist_elements =  resource.find_all(name="div", attrs={"class":"paperlist"}) 
    if len(paperlist_elements) == 0:
        crawl_result_list.append(PAPERLIST_ZERO_QUOTE)
        return crawl_result_list





    for paperlist_element in paperlist_elements:
        p_element = paperlist_element.find(name="p", attrs = {"class":"num"})
        page = p_element.get_text()
        match_object = re.search('\d+', page)
        if match_object == None:
            crawl_result_list.append(PAGE_ZERO_QUOTE)
            return crawl_result_list

        page = int(match_object.group())
        
        a_elements = paperlist_element.find_all(name = "a")
        for a_element in a_elements:
            news = {}
            title = a_element.get_text().strip()
            news['company_name'] = 'munhwa'
            news['title'] = title
            news['page'] = page
            news['date'] = date
            

            if "[" in title and "]" in title:
                inside_bracket = title.split('[',1)[1].split(']')[0]
                if title.split('[')[0] == '' and title.split(']')[1] == '':
                    numOfAd = numOfAd + 1
                    continue
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



    if numOfHeadline == 0:
        crawl_result_list.append(HEADLINE_ZERO_QUOTE)
        return crawl_result_list
    else:
        failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2)

    report = {}
    report['date'] = date
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
    return crawl_result_list





def kmib(date):
    """crawls title and link from kmib and naver site, and stores (company_name, date, page, title, link) into db"""

    crawl_result_list = []

    kmib_url = KMIB_URL + "?PaperDate=" + date
    date = int(date.replace("-",""))

    response = requests.get(kmib_url)
    if response.status_code != 200:
        crawl_result_list.append(RESPONSE_ERROR_QUOTE)
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
        return crawl_result_list

    #below code extracts title 
    for paperlist_element in paperlist_elements:
        p_element = paperlist_element.find(name="p", attrs = {"class":"num"})
        page = p_element.get_text()
        match_object = re.search('\d+', page)
        if match_object == None:
            crawl_result_list.append(PAGE_ZERO_QUOTE)
            return crawl_result_list

        page = int(match_object.group())       

        a_elements = paperlist_element.find_all(name = "a")
        for a_element in a_elements:
            news = {}
            news['company_name'] = 'kmib'
            title = a_element.get_text().strip()
            news['title'] = title
            news['page'] = page
            news['date'] = date
            

            if "[" in title and "]" in title:
                inside_bracket = title.split('[',1)[1].split(']')[0]
                if title.split('[')[0] == '' and title.split(']')[1] == '':
                    numOfAd = numOfAd + 1
                    continue
                title = title.replace("["+inside_bracket+"]","")

            title_encoded = urllib.parse.quote(title)
            url = NAVER_SEARCH_URL + title_encoded
            response = requests.get(url)
            resource = BeautifulSoup(response.text,features = "html.parser")
            a_element = resource.find(name ="a", attrs ={ "class":"_sp_each_title"})
            if a_element != None:
                link =  a_element.get('href')
                if link.find("kmib") == -1:
                    numOfWrongMedia = numOfWrongMedia + 1
                    news['link'] = None
                else:
                    news['link'] = link
            else:
                news['link'] = None
                numOfNone = numOfNone + 1

            news_list.append(news)
            numOfHeadline = numOfHeadline + 1


    if numOfHeadline == 0:
        crawl_result_list.append(HEADLINE_ZERO_QUOTE)
        return crawl_result_list
    else:
        failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2)

    report = {}
    report['date'] = date
    report['news'] = 'kmib'
    report['whole'] = numOfHeadline
    report['none'] = numOfNone + numOfWrongMedia
    report['failure'] = failure_percentage
    
    sql_handler.inserts_news_list('kmib', news_list)
    sql_handler.inserts_report(report)

    success_quotes = []
    success_quotes.append("number of none: " + str(numOfNone))
    success_quotes.append("number of msmatched news: " + str(numOfWrongMedia))
    success_quotes.append("number of ads: " + str(numOfAd))
    success_quotes.append("number of headline: " + str(numOfHeadline))
    success_quotes.append("failure percentage: " + str(failure_percentage) + "%")
    
    crawl_result_list.extend(success_quotes)
    return crawl_result_list




def seoul(date):
    """crawls title from seoul economic and link from naver, and stores (company_name, date, page, title, link) into db"""

    crawl_result_list = []

    seoul_url = SEOUL_URL + "?PaperDate=" + date
    date_with_dash = date
    date = int(date.replace("-",""))
    
    response = requests.get(seoul_url)
    if response.status_code != 200:
        crawl_result_list.append(RESPONSE_ERROR_QUOTE)
        return crawl_result_list  
    resource = BeautifulSoup(response.text,features = "html.parser")
   
    

    #below code crawls how many bottom pages are in at seoul economic site
    a_elements = resource.find_all(name = "a", attrs = {"style" : "padding-top:2px;cursor:hand"})
    if len(a_elements) == 0:
        crawl_result_list.append(PAGE_ZERO_QUOTE)
        return crawl_result_list
    page_list = []
    for a_element in a_elements:
        href = a_element.get("href")
        page_number = int(href.split("(")[1].split(")")[0])
        page_list.append(page_number)
    max_page_number = max(page_list)

    #Now code of extracting titles starts
    news_list = []
    numOfWrongMedia = 0
    numOfAd = 0
    numOfNone = 0
    numOfHeadline = 0

    for searchpage in range(1, max_page_number+1):
        response = requests.post(SEOUL_URL+"?PaperDate="+date_with_dash, data = {"searchpage": searchpage, "searchdate":date_with_dash})
        if response.status_code != 200:
            crawl_result_list.append(RESPONSE_ERROR_QUOTE)
            return crawl_result_list

        resource = BeautifulSoup(response.text,features = "html.parser")
        paperlist_elements =  resource.find_all(name="div", attrs={"class":"paperlist"})    
        if len(paperlist_elements) == 0:
            crawl_result_list.append(PAPERLIST_ZERO_QUOTE)
            return crawl_result_list

        for paperlist_element in paperlist_elements:

            p_element = paperlist_element.find(name="p", attrs = {"class":"num"})
            page = p_element.get_text()
            match_object = re.search('\d+', page)
            if match_object == None:
                crawl_result_list.append(PAGE_ZERO_QUOTE)
                return crawl_result_list

            page = int(match_object.group())
            
            a_elements = paperlist_element.find_all(name = "a")
            for a_element in a_elements:
                news = {}
                title = a_element.get_text().strip()

                news['company_name'] = 'seoul'
                news['title'] = title
                news['page'] = page
                news['date'] = date
                
                

                if "[" in title and "]" in title:
                    inside_bracket = title.split('[',1)[1].split(']')[0]
                    if title.split('[')[0] == '' and title.split(']')[1] == '':
                        numOfAd = numOfAd + 1
                        continue
                    title = title.replace("["+inside_bracket+"]","")

                title_encoded = urllib.parse.quote(title)
                url = NAVER_SEARCH_URL + title_encoded
                response = requests.get(url)
                resource = BeautifulSoup(response.text,features = "html.parser")
                a_element = resource.find(name ="a", attrs ={ "class":"_sp_each_title"})
                if a_element != None:
                    link =  a_element.get('href')
                    if link.find("sedaily") == -1:
                        numOfWrongMedia = numOfWrongMedia + 1
                        news['link'] = None
                    else:
                        news['link'] = link
                else:
                    news['link'] = None
                    numOfNone = numOfNone + 1

                news_list.append(news)
                numOfHeadline = numOfHeadline + 1

    
    
    if numOfHeadline == 0:
        crawl_result_list.append(HEADLINE_ZERO_QUOTE)
        return crawl_result_list
    else:
        failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2)
    
    report = {}
    report['date'] = date
    report['news'] = 'seoul'
    report['whole'] = numOfHeadline
    report['none'] = numOfNone + numOfWrongMedia
    report['failure'] = failure_percentage

    sql_handler.inserts_news_list('seoul', news_list)
    sql_handler.inserts_report(report)

    success_quotes = []
    success_quotes.append("number of none: " + str(numOfNone))
    success_quotes.append("number of msmatched news: " + str(numOfWrongMedia))
    success_quotes.append("number of ads: " + str(numOfAd))
    success_quotes.append("number of headline: " + str(numOfHeadline))
    success_quotes.append("failure percentage: " + str(failure_percentage) + "%")
    
    crawl_result_list.extend(success_quotes)
    return crawl_result_list

    
    

    


def mk(date):
    """crawls title from maeil economy and link from naver, and stores (company_name, date, page, title, link) into db"""

    crawl_result_list = []
    
    mk_url = MK_URL + "?PaperDate=" + date
    date = int(date.replace("-",""))

    response = requests.get(mk_url)
    if response.status_code != 200:
        crawl_result_list.append(RESPONSE_ERROR_QUOTE)
        return crawl_result_list  
    resource = BeautifulSoup(response.text,features = "html.parser")
   
    

    #below code crawls how many bottom pages are in at seoul economic site
    a_elements = resource.find_all(name = "a", attrs = {"style" : "padding-top:2px;cursor:hand"})
    if len(a_elements) == 0:
        crawl_result_list.append(PAGE_ZERO_QUOTE)
        return crawl_result_list
    page_list = []
    for a_element in a_elements:
        href = a_element.get("href")
        page_number = int(href.split("(")[1].split(")")[0])
        page_list.append(page_number)
    max_page_number = max(page_list)
    
    

    #Now code of extracting titles starts
    news_list = []
    numOfWrongMedia = 0
    numOfAd = 0
    numOfPage = 1
    numOfNone = 0
    numOfHeadline = 0

    for page_button in range(1, max_page_number+1):
        response = requests.get(mk_url+"&page=" +str(page_button))
        if response.status_code != 200:
            crawl_result_list.append(RESPONSE_ERROR_QUOTE)
            return crawl_result_list

        resource = BeautifulSoup(response.text,features = "html.parser")
        paperlist_elements =  resource.find_all(name="div", attrs={"class":"paperlist"})    
        if len(paperlist_elements) == 0:
            crawl_result_list.append(PAPERLIST_ZERO_QUOTE)
            return crawl_result_list

        for paperlist_element in paperlist_elements:
            p_element = paperlist_element.find(name="p", attrs = {"class":"num"})
            page = p_element.get_text()
            match_object = re.search('\d+', page)
            if match_object == None:
                crawl_result_list.append(PAGE_ZERO_QUOTE)
                return crawl_result_list

            page = int(match_object.group())

            a_elements = paperlist_element.find_all(name = "a")
            for a_element in a_elements:
                news = {}
                news['company_name'] = 'mk'
                title = a_element.get_text().strip()
                news['title'] = title
                news['page'] = page
                news['date'] = date
                

                if "[" in title and "]" in title:
                    inside_bracket = title.split('[',1)[1].split(']')[0]
                    if title.split('[')[0] == '' and title.split(']')[1] == '':
                        numOfAd = numOfAd + 1
                        continue
                    title = title.replace("["+inside_bracket+"]","")

                title_encoded = urllib.parse.quote(title)
                url = NAVER_SEARCH_URL + title_encoded
                response = requests.get(url)
                resource = BeautifulSoup(response.text,features = "html.parser")
                a_element = resource.find(name ="a", attrs ={ "class":"_sp_each_title"})
                if a_element != None:
                    link =  a_element.get('href')
                    if link.find("mk") == -1:
                        numOfWrongMedia = numOfWrongMedia + 1
                        news['link'] = None
                    else:
                        news['link'] = link
                else:
                    news['link'] = None
                    numOfNone = numOfNone + 1
                news_list.append(news)
                numOfHeadline = numOfHeadline + 1

    
    
    if numOfHeadline == 0:
        crawl_result_list.append(HEADLINE_ZERO_QUOTE)
        return crawl_result_list
    else:
        failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2)
    
    report = {}
    report['date'] = date
    report['news'] = 'mk'
    report['whole'] = numOfHeadline
    report['none'] = numOfNone + numOfWrongMedia
    report['failure'] = failure_percentage
       
    sql_handler.inserts_news_list('mk', news_list)
    sql_handler.inserts_report(report)

    success_quotes = []
    success_quotes.append("number of none: " + str(numOfNone))
    success_quotes.append("number of msmatched news: " + str(numOfWrongMedia))
    success_quotes.append("number of ads: " + str(numOfAd))
    success_quotes.append("number of headline: " + str(numOfHeadline))
    success_quotes.append("failure percentage: " + str(failure_percentage) + "%")
    
    crawl_result_list.extend(success_quotes)
    return crawl_result_list



