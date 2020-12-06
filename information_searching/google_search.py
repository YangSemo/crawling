from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver

baseUrl = 'https://www.google.com/search?q='
plusUrl = input('무엇을 검색할까요? :')
url = baseUrl + quote_plus(plusUrl)

# 구글 크롬 실행
driver = webdriver.Chrome('C:/Users/SAMSUNG/chromedriver_win32/chromedriver.exe')
driver.get(url)

html = driver.page_source # 현재 페이지
soup = BeautifulSoup(html,'html.parser')

g = soup.select('.g') # g 클래스를 select
# select의 type는 list

for i in g:
    # select_one으로 해야 text 형식이 가능
    print(i.select_one('h3').text) # 제목
    print(i.select_one('.s').text) # 요약본
    print(i.a.attrs['href']) # 주소
    print()
#
# driver.close()
