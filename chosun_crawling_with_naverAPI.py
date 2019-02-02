import requests
from bs4 import BeautifulSoup
import urllib.parse

naver_search_url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query="
naver_api_url="https://openapi.naver.com/v1/search/news.xml?"
sim = "&sort=sim"

response = requests.get("http://srchdb1.chosun.com/pdf/i_service/index_new.jsp")


print("typeof(response.text): ", type(response.text))

tag = BeautifulSoup(response.text)
ss_list_elements =  tag.find_all(name="div", attrs={"class":"ss_list"})


numOfPage = 1
numOfAd = 0
numOfNone = 0
numOfHeadline = 0
numOfWrongMedia = 0
for ss_list_element in ss_list_elements:
    li_elements = ss_list_element.find_all(name = "li")
    #print("typeof(element.find_all(name='li')) is: ", type(ul))
    #print("len of find_all(name='li') is: ", len(ul))
    print(str(numOfPage) + "면")
    for li_element in li_elements:
        title = li_element.get_text()
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
        

        #if title.find("…") != -1:
            #title = title.replace("…"," ")
   
        title_encoded = urllib.parse.quote(title)
        news = "query=" + title
        url = naver_api_url + news + sim
        response =  requests.get(url, headers= {"X-Naver-Client-Id":"kNXNpK9fnkCxGK9rPz45",  "X-Naver-Client-Secret": "96h4HYH1DW"}) 
        resource = BeautifulSoup(response.text, features = "xml")
        originalLink_element = resource.find(name="originallink")
        if originalLink_element != None:
            if originalLink_element.string.find("chosun") == -1:
                numOfWrongMedia += 1
            else:
                print(originalLink_element.string)
        else:
            print("orinallink is none")
            numOfNone += 1

        numOfHeadline += 1


    numOfPage = numOfPage + 1
    print("")
    #if num == 10: break

failure_percentage = round((numOfNone + numOfWrongMedia) /numOfHeadline * 100, 2
)
print("number of mismatched news: ", numOfWrongMedia)
print("number of none : ", numOfNone)
print("number of news headline: " , numOfHeadline)
print("failure percentage: ", failure_percentage, "%")
