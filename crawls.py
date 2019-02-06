import requests
from bs4 import BeautifulSoup
import urllib.parse
import sqlite3
from datetime import date
import sql_handler

NAVER_SEARCH_URL = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
CHOSUN_URL = "http://srchdb1.chosun.com/pdf/i_service/index_new.jsp"

DONGA_URL = "http://news.donga.com/Pdf"





'''function that crawls chousn site'''

def chosun(): 
    """crawls news headline from chosun, and link from naver, then adds 
    (date, page, title, link) to the database."""

    print("CHOSUN CRAWLING STARTS!")
    response = requests.get(CHOSUN_URL)
    if response.status_code != 200:
        print("Error: response error")
        return

    news_list = []
    numOfWrongMedia = 0
    numOfAd = 0
    numOfPage = 1
    numOfNone = 0
    numOfHeadline = 0

    resource = BeautifulSoup(response.text,features = "html.parser")

    ss_list_elements =  resource.find_all(name="div", attrs={"class":"ss_list"})
    if len(ss_list_elements) == 0:
        print("Error: number of ss_list_elements are zero.")
        return

    for ss_list_element in ss_list_elements:
        li_elements = ss_list_element.find_all(name = "li")
        #print("typeof(element.find_all(name='li')) is: ", type(ul))
        #print("len of find_all(name='li') is: ", len(ul))
        for li_element in li_elements:
            news = {}
            title = li_element.get_text()
            news['title'] = title
            news['page'] = numOfPage

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


    sql_handler.insert('chosun', news_list)

    if numOfHeadline == 0:
        print("Error: number of headline is 0.")
        return
    else:
        failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2)

    print("number of none: ", numOfNone)
    print("number of mismatched news: ", numOfWrongMedia)
    print("number of ads: ", numOfAd)
    print("number of headline: " , numOfHeadline)
    print("failure percentage: ", failure_percentage, "%")




def donga():
    """crawls news headline from donga, and link from naver, then adds 
    (date, page, title, link) to the database."""
    
    print("DONGA CRAWLING STARTS!")

    response = requests.get(DONGA_URL)
    if response.status_code != 200:
        print("Error: response error")
        return
    
    resource = BeautifulSoup(response.text, features = "html.parser")
    section_list_element = tag.find(name = "ul", attrs={"class":"section_list"})
    
    if len(section_list_element) == 0:
        print("Error: number of section_list_element is zero")
        return

    section_txt_elements =  section_list_element.find_all(name="div", attrs={"class":"section_txt"})
    
    if len(section_txt_elements) == 0:
        print("Error: number of section_txt_elements is zero")
        return
    
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

    sql_handler.insert('donga', news_list)
    print("number of headline: ", numOfHeadline)
    print("number of ad: ", numOfAd)
