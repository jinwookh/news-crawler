import requests
from bs4 import BeautifulSoup
import urllib.parse

naver_api_url="https://openapi.naver.com/v1/search/news.xml?"
sim = "&sort=sim"


response = requests.get("http://www.paoin.com/service/Kukinews/Default.aspx")
tag = BeautifulSoup(response.text,features = "html.parser")
paperlist_elements = tag.find_all(name="div", attrs={"class":"paperlist"})


numOfPage = 1
numOfNone = 0
numOfHeadline = 0
numOfWrongMedia = 0
numOfAd = 0
for paperlist_element in paperlist_elements:
    a_elements = paperlist_element.find_all(name = "a")
    print(str(numOfPage) + "면")
    for a_element in a_elements:
        title = a_element.get_text().strip()
        print(title)


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
            if originalLink.find("kmib") == -1:
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
print("number of headline: " , numOfHeadline)
print("failure percentage: ", failure_percentage, "%")
