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
for element in found:
    ul = element.find_all(name = "li")
    #print("typeof(element.find_all(name='li')) is: ", type(ul))
    #print("len of find_all(name='li') is: ", len(ul))
    print(str(num) + "면")
    for title in ul:
        title_to_string = title.get_text()
        print(title_to_string)
        title_to_string_encoded = urllib.parse.quote(title_to_string)
        url = naver_search_url + title_to_string_encoded
        response = requests.get(url)
        resource = BeautifulSoup(response.text,features = "html.parser")
        news_element = resource.find(name ="a", attrs ={ "class":"_sp_each_title"})
        if news_element != None:
            link =  news_element.get('href')
            if link.find("chosun") == -1:
                numOfWrongMedia = numOfWrongMedia + 1
                print(resource.prettify())
            print("The link is: ", link)
        else:
            print("The link is none")
            numOfNone = numOfNone + 1
        numOfHeadline = numOfHeadline + 1
    

    num = num + 1
    print("")

print("number of none: ", numOfNone)
print("number of mismatched news: ", numOfWrongMedia)
print("number of headline: " , numOfHeadline)
        
