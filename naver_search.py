import requests
import bs4

news = "query=" + "미세먼지 대책"
url = "https://openapi.naver.com/v1/search/news.xml?"

sim = "&sort=sim"

url = url + news + sim

user = "kNXNpK9fnkCxGK9rPz45"

password = "96h4HYH1DW"

response =  requests.get(url, headers= {"X-Naver-Client-Id":"kNXNpK9fnkCxGK9rPz45",  "X-Naver-Client-Secret": "96h4HYH1DW"})
print("type of request.get(url): ", type(response))
print(response)
print("response.content is: ", response.content)
print("response.text is: ", response.text)

resource = bs4.BeautifulSoup(response.text)
print("resource.prettify() is: ",resource.prettify())




