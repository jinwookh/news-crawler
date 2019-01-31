import requests
from bs4 import BeautifulSoup
import urllib.parse


response = requests.get("http://news.donga.com/Pdf")

tag = BeautifulSoup(response.text,features = "html.parser")
section_list_element = tag.find(name="ul", attrs={"class":"section_list"})
section_txt_elements =  section_list_element.find_all(name="div", attrs={"class":"section_txt"})


numOfPage = 1
numOfNone = 0
numOfHeadline = 0
numOfAd = 0
for section_txt_element in section_txt_elements:
    li_elements = section_txt_element.find_all(name = "li")
    tit_element = section_txt_element.find(name = "span")

  
 
    print(tit_element.get_text())
    for li_element in li_elements:
        title = li_element.get_text()
        print(title)
        a_element = li_element.find(name="a")
        if a_element == None:
            print("Above title is ad, so there is no link.")
            numOfAd += 1
        else:
            link = a_element.get('href')
            print(link)

        numOfHeadline += 1
       
    numOfPage += 1
    print("")
print("number of headline: ", numOfHeadline)
print("number of ad: ", numOfAd)
