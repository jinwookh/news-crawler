import requests
from bs4 import BeautifulSoup
import urllib.parse

naver_api_url="https://openapi.naver.com/v1/search/news.xml?"
sim = "&sort=sim"

response = requests.get("http://paoin.khan.co.kr/service/Khan/Default.aspx")
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
        news = "query=" + title
        url = naver_api_url + news + sim
        response =  requests.get(url, headers= {"X-Naver-Client-Id":"kNXNpK9fnkCxGK9rPz45",  "X-Naver-Client-Secret": "96h4HYH1DW"}) 
        resource = BeautifulSoup(response.text, features = "xml")
        originalLink_element = resource.find(name="originallink")
        if originalLink_element != None:
            originalLink = originalLink_element.string
            if originalLink.find("khan") == -1:
                numOfWrongMedia += 1
            print(originalLink)

        else:
            print("orinallink is none")
            numOfNone += 1

        numOfHeadline += 1           
            
            

    numOfPage = numOfPage + 1
    print("")

failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2)

print("number of none: ", numOfNone)
print("number of mismatched news: ", numOfWrongMedia)
print("number of ads: ", numOfAd)
print("number of headline: ", numOfHeadline)
print("failure percentage: ", failure_percentage, "%")
