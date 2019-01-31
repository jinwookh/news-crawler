import requests
from bs4 import BeautifulSoup
import urllib.parse

naver_search_url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query="
user = "kNXNpK9fnkCxGK9rPz45"

response = requests.get("http://srchdb1.chosun.com/pdf/i_service/index_new.jsp")



tag = BeautifulSoup(response.text,features = "html.parser")
found =  tag.find_all(name="div", attrs={"class":"ss_list"})

num = 1
numOfNone = 0
numOfHeadline = 0
numOfWrongMedia = 0
numOfAds = 0
for element in found:
    ul = element.find_all(name = "li")
    #print("typeof(element.find_all(name='li')) is: ", type(ul))
    #print("len of find_all(name='li') is: ", len(ul))
    print(str(num) + "면")
    for title in ul:
        title_to_string = title.get_text()
        print(title_to_string)

        #below code is for handling title with bracket([])
        #since search is not successful with title with bracket,
        #we will try removing bracket from title if title does not contatin
        #'전면광고'
        if "[" in title_to_string and "]" in title_to_string:
            inside_bracket = title_to_string.split('[',1)[1].split(']')[0]
            if inside_bracket != "전면광고":
                title_to_string = title_to_string.replace(inside_bracket,"")
            else:
                numOfAds = numOfAds + 1


        title_to_string_encoded = urllib.parse.quote(title_to_string)
        url = naver_search_url + title_to_string_encoded
        response = requests.get(url)
        resource = BeautifulSoup(response.text,features = "html.parser")
        news_element = resource.find(name ="a", attrs ={ "class":"_sp_each_title"})
        if news_element != None:
            link =  news_element.get('href')
            if link.find("chosun") == -1:
                numOfWrongMedia = numOfWrongMedia + 1
                print("Below link does not belong to chosun")
            print("The link is: ", link)
        else:
            print("The link is none")
            numOfNone = numOfNone + 1
        numOfHeadline = numOfHeadline + 1
    

    num = num + 1
    print("")

print("number of none: ", numOfNone)
print("number of mismatched news: ", numOfWrongMedia)
print("number of ads: ", numOfAds)
print("number of headline: " , numOfHeadline)

        
