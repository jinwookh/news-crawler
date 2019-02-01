import requests
from bs4 import BeautifulSoup
import urllib.parse

naver_search_url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="

response = requests.get("http://www.paoin.com/service/Munhwa/Default.aspx")
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
        url = naver_search_url + title_encoded
        response = requests.get(url)
        resource = BeautifulSoup(response.text,features = "html.parser")
        news_element = resource.find(name ="a", attrs ={ "class":"_sp_each_title"})
        if news_element != None:
            link =  news_element.get('href')
            if link.find("munhwa") == -1:
                numOfWrongMedia = numOfWrongMedia + 1
                print("Below link does not belong to munhwa")
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
print("number of headline: " , numOfHeadline)
print("failure percentage: ", failure_percentage, "%")
