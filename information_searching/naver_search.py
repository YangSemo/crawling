import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import re

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
< naver 뉴스(블로그, 카페 등) 검색시 리스트 크롤링하는 프로그램 > _select사용
- 크롤링 해오는 것 : 링크,제목,신문사,날짜,내용요약본
- 날짜,내용요약본  -> 정제 작업 필요
- 리스트 -> 딕셔너리 -> df -> 엑셀로 저장 
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#각 크롤링 결과 저장하기 위한 리스트 선언
title_text=[]
link_text=[]
source_text=[]
date_text=[]
contents_text=[]
result={}

#엑셀로 저장하기 위한 변수
RESULT_PATH = 'C:/Users/SAMSUNG/PycharmProjects/crawling/naver_excel_file/'  # 결과 저장할 경로
now = datetime.now() #파일이름 현 시간으로 저장하기

# 날짜 정제화 함수
def date_refine(test):
    try:
        #지난 뉴스
        #머니투데이  10면 1단  2018.11.05.  네이버뉴스   보내기
        pattern = '\d+.(\d+).(\d+).' #정규표현식

        r = re.compile(pattern)
        match = r.search(test).group(0)  # 2018.11.05.
        date_text.append(match)

    except AttributeError:
        # 최근 뉴스
        # 이데일리  1시간 전  네이버뉴스   보내기
        pattern = '\w* (\d\w*)'  # 정규표현식

        r = re.compile(pattern)
        match = r.search(test).group(1)
        date_text.append(match)

# 내용 정제화 함수
def contents_refine(contents):
        first_refine = re.sub('<dl>.*?</a> </div> </dd> <dd>', '',
                                      str(contents)).strip()  #앞에 필요없는 부분 제거
        second_refine = re.sub('<ul class="relation_lst">.*?</dd>', '',
                                       first_refine).strip()#뒤에 필요없는 부분 제거 (새끼 기사)
        third_refine = re.sub('<.+?>', '', second_refine).strip()
        contents_text.append(third_refine)

def crawler(maxpage, query, sort, s_date, e_date):
    s_from = s_date.replace(".","")
    e_to = e_date.replace(".","")
    page = 1

    # 11= 2페이지 21=3페이지 31=4페이지  ...81=9페이지 , 91=10페이지, 101=11페이지
    maxpage_t = (int(maxpage)-1)*10+1

    while page <= maxpage_t:
        # url의 where=' '부분 수정하여 블로그, 카페 검색 가능
        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=" + sort + "&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(
                page)
        res = requests.get(url)
        soup = BeautifulSoup(res.content,'html.parser')

        # <a>태그에서 제목과 링크주소 추출
        a_tags = soup.select('._sp_each_title') # select는 모든 태그 선택
        for a_tag in a_tags:
            title_text.append(a_tag.text) # 제목
            link_text.append(a_tag['href']) # 링크주소

        # 신문사 추출
        source_lists = soup.select('._sp_each_source')
        for source_list in source_lists:
            source_text.append(source_list.text) # 신문사

        # 날짜 추출
        date_lists = soup.select('.txt_inline')
        for date_list in date_lists:
            before_refine = date_list.text
            date_refine(before_refine) # 날짜 정제 함수 사용

        # 본문 요약본
        contents_lists = soup.select('ul.type01 dl')
        for contents_list in contents_lists:
            # print('==='*40)
            # print(contents_list)
            contents_refine(contents_list)  # 본문요약 정제화

        # 모든 리스트 딕셔너리 형태로 저장
        result = {"date": date_text, "title": title_text, "source": source_text, "contents": contents_text,
                  "link": link_text}
        print(page)

        df = pd.DataFrame(result) # 테이블 형식으로 변환
        print(df)
        page+=10

        # 새로 만들 엑셀 파일 이름 지정정
        outputFileName = query+'('+'%s-%s-%s  %s시 %s분 %s초 merging).xlsx' %\
        (now.year, now.month, now.day, now.hour, now.minute, now.second)
        df.to_excel(RESULT_PATH + outputFileName, sheet_name="first_crawling")


def main():
    info_main = input("=" * 50 + "\n" + "입력 형식에 맞게 입력해주세요." + "\n" + " 시작하시려면 Enter를 눌러주세요." + "\n" + "=" * 50)

    maxpage = input("최대 크롤링할 페이지 수 입력하시오: ")
    query = input("검색어 입력: ")
    sort = input("뉴스 검색 방식 입력(관련도순=0  최신순=1  오래된순=2): ")  # 관련도순=0  최신순=1  오래된순=2
    s_date = input("시작날짜 입력(2019.01.04):")  # 2019.01.04
    e_date = input("끝날짜 입력(2019.01.05):")  # 2019.01.05

    crawler(maxpage, query, sort, s_date, e_date)


main()