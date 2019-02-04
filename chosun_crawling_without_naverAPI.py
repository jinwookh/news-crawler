import requests
from bs4 import BeautifulSoup
import urllib.parse
import sqlite3
from datetime import date
import sql_handler


naver_search_url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
response = requests.get("http://srchdb1.chosun.com/pdf/i_service/index_new.jsp?Y=2019&M=02&D=02")
news_list = []
numOfWrongMedia = 0
numOfAd = 0
numOfPage = 1
numOfNone = 0
numOfHeadline = 0


tag = BeautifulSoup(response.text,features = "html.parser")
ss_list_elements =  tag.find_all(name="div", attrs={"class":"ss_list"})

for ss_list_element in ss_list_elements:
    li_elements = ss_list_element.find_all(name = "li")
    #print("typeof(element.find_all(name='li')) is: ", type(ul))
    #print("len of find_all(name='li') is: ", len(ul))
    print(str(numOfPage) + "면")
    for li_element in li_elements:
        news = {}
        title = li_element.get_text()
        news['title'] = title
        news['page'] = numOfPage
        print(title)

        #below code is for handling title with bracket([])
        #since search is not successful with title with bracket,
        #we will try removing bracket from title if title does not contatin
        #'전면광고'

        if "[" in title and "]" in title:
            inside_bracket = title.split('[',1)[1].split(']')[0]
            if title.find('전면광고') != -1:
                numOfAd = numOfAd + 1
                news['link'] = None
                print("Above title is ad or sth that is not article")
                break
            title = title.replace("["+inside_bracket+"]","")


        title_encoded = urllib.parse.quote(title)
        url = naver_search_url + title_encoded
        response = requests.get(url)
        resource = BeautifulSoup(response.text,features = "html.parser")
        a_element = resource.find(name ="a", attrs ={ "class":"_sp_each_title"})

        if a_element != None:
            link =  a_element.get('href')
            if link.find("chosun") == -1:
                numOfWrongMedia = numOfWrongMedia + 1
                news['link'] = None
                print("Below link does not belong to chosun")
            else:
                news['link'] = link    
            print("The link is: ", link)
        else:
            news['link'] = None
            print("The link is none")

            numOfNone = numOfNone + 1
        print('news: ', news)
        news_list.append(news)
        numOfHeadline = numOfHeadline + 1
    

    numOfPage = numOfPage + 1
    print("")


sql_handler.insert('chosun', news_list)

failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2)

print("number of none: ", numOfNone)
print("number of mismatched news: ", numOfWrongMedia)
print("number of ads: ", numOfAd)
print("number of headline: " , numOfHeadline)
print("failure percentage: ", failure_percentage, "%")
        
