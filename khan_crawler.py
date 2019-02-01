import requests
from bs4 import BeautifulSoup
import urllib.parse

naver_search_url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="

response = requests.get("http://paoin.khan.co.kr/service/Khan/Default.aspx")
print(response)
tag = BeautifulSoup(response.text,features = "html.parser")
article_elements =  tag.find_all(name="div", attrs={"class":"article"})

numOfPage = 1
numOfNone = 0
numOfHeadline = 0
numOfWrongMedia = 0
numOfAd = 0
for article_element in article_elements:
    list_elements = article_element.find_all(name = "li")
    print(str(numOfPage) + "면")
    for list_element in list_elements:
        a_element = list_element.find(name = "a")
        title = a_element.get("title")
        if title == "":
            title = a_element.get_text().strip()
        
        print(title)

        #below code is for handling title with bracket([])
        #since search is not successful with title with bracket,
        #we will try removing bracket from title if title does not contatin
        #'광고'
        if "[" in title and "]" in title:
            inside_bracket = title.split('[',1)[1].split(']')[0]
            if title.split('[')[0] == '' and title.split(']')[1] == '':
                numOfAd = numOfAd + 1
                print("Above title is ad or sth that is not article")
                break
            title = title.replace("["+inside_bracket+"]","")

        title_encoded = urllib.parse.quote(title)
        url = naver_search_url + title_encoded 
        response = requests.get(url)
        resource = BeautifulSoup(response.text,features = "html.parser")
        _sp_each_title_element = resource.find(name ="a", attrs ={ "class":"_sp_each_title"})
        if _sp_each_title_element != None:
            link =  _sp_each_title_element.get('href')
            if link.find("khan") == -1:
                numOfWrongMedia = numOfWrongMedia + 1
                print("Below link does not belong to khan")
            print("The link is: ", link)
        else:
            print("The link is none")
            numOfNone = numOfNone + 1
        numOfHeadline = numOfHeadline + 1

    numOfPage = numOfPage + 1
    print("")

failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2)

print("number of none: ", numOfNone)
print("number of mismatched news: ", numOfWrongMedia)
print("number of ads: ", numOfAd)
print("number of headline: ", numOfHeadline)
print("failure percentage: ", failure_percentage, "%")
