import requests
from bs4 import BeautifulSoup
import urllib.parse

naver_search_url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query="
naver_api_url="https://openapi.naver.com/v1/search/news.xml?"
user = "kNXNpK9fnkCxGK9rPz45"
password ="96h4HYH1DW"
sim = "&sort=sim"

response = requests.get("http://srchdb1.chosun.com/pdf/i_service/index_new.jsp")


print("typeof(response.text): ", type(response.text))
print("typeof(response.content): ", type(response.content))

tag = BeautifulSoup(response.text)
found =  tag.find_all(name="div", attrs={"class":"ss_list"})
print("what is find: ", tag.find_all(name="div", attrs={"class" :"ss_list"}))
print("checkout find[0]: ", found[0])
print("checkout type of find[0]", type(found[0]))
print("checkout found[0].get_text(): " , found[0].get_text())


num = 1
numOfNone = 0
numOfHeadline = 0
for element in found:
    ul = element.find_all(name = "li")
    #print("typeof(element.find_all(name='li')) is: ", type(ul))
    #print("len of find_all(name='li') is: ", len(ul))
    print(str(num) + "면")
    for title in ul:
        title_to_string = title.get_text()
        print(title_to_string)
        if title_to_string.find("…") != -1:
            print("above title contains '...'")
            title_to_string = title_to_string.replace("…","")
        title_to_string_encoded = urllib.parse.quote(title_to_string)
        news = "query=" + title_to_string
        url = naver_api_url + news + sim
        response =  requests.get(url, headers= {"X-Naver-Client-Id":"kNXNpK9fnkCxGK9rPz45",  "X-Naver-Client-Secret": "96h4HYH1DW"}) 
        resource = BeautifulSoup(response.text, features = "xml")
        originalLink = resource.find(name="originallink")
        if originalLink != None:
            if originalLink.string.find("chosun") == -1:
                print(resource.prettify())
            print("originallink to string: ",originalLink.string)
        else:
            print("orinallink is none")
            numOfNone += 1
        '''
            another_url = naver_search_url + title_to_string_encoded
            response_of_search_url = requests.get(another_url)
            print("response_of_search_url: ", response_of_search_url) 
            resource_of_search_url = BeautifulSoup(response_of_search_url.text, features = "html.parser")
            print("another_url : ", another_url)
            print("title_to_string : ", title_to_string)
            news_element_of_another_url = resource_of_search_url.find(attrs = {"class": "_sp_each_title"})
            print("news_element_of_another_url: ", news_element_of_another_url)
            link_of_news_element_of_another_url = news_element_of_another_url.get('href')
            if link_of_news_element_of_another_url == None or link_of_news_element_of_another_url.find("chosun") == -1:
                print("originallink is None. ")
                numOfNone += 1
            else:
                print("originallink is: ", link_of_news_element_of_another_url)'''
            
        #print("type of originallink: ", type(originalLink))
        numOfHeadline += 1


        '''if originalLink_to_text.find("chosun"):
            print("link: ", originalLink_to_text)
        else:
            print("link: none")'''
    #title = element.get_text()
    #splited_title = title.split('\n')
    #print ( str(num) + "면")
    #print ("titles: " , title)
    #print("splited title: ", splited_title)
    #news = "query=" + element.get_text()
    num = num + 1
    print("\n")
    #if num == 10: break
print("number of none : ", numOfNone)
print("number of news headline: " , numOfHeadline)
