from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import csv

# csv 파일명
# csv_file_name = './본사_성장성/외식.csv'
# csv_file_name = './본사_성장성/도소매.csv'
csv_file_name = './본사_성장성/서비스.csv'

# 대분류 value값
# selUpjong_value = '21'
# selUpjong_value = '22'
selUpjong_value = '23'

# 대분류 한글명
# selUpjong_kor='외식'
# selUpjong_kor='도소매'
selUpjong_kor='서비스'

# 중분류 리스트(value값)
# selIndus_list = ['A1','B1','C1','D1','E1','F1','G1','H1','I1','J1','K1','L1','M1','N1','O1']
# selIndus_list = ['A2','B2','C2','D2','E2','F2','G2']
selIndus_list = ['A3','B3','C3','D3','E3','F3','G3','O ','H3','I3','J3','K3','L3','M3','N3','O3','P3','Q3','R3','S3','T3','U3']

# 중분류 리스트(한글명)
# mid_select = ['한식','분식','중식','일식','서양식','기타외국식','패스트푸드','치킨','피자','제과제빵','아이스크림_빙수','커피','음료','주점','기타외식']
# mid_select = ['편의점', '의류패션','화장품','농수산물','건강식품','종합소매점','기타도소매']
mid_select = ['교육_교과','교육_외국어','교육_기타','교육외_유아','부동산중개','임대','숙박','유아','스포츠','이미용','자동차','PC방','오락','배달','안경','세탁','이사','운송','반려동물','약국','인력파견','기타서비스']

# 비교항목(성장성, 안정성, 수익성)
item = 'listHq01'
# item = 'listHq02'
# item = 'listHq03'

# csv 파일로 저장
# 컬럼명
column_list = ['업종(대)','업종(중)', '상호', '매출액','매출액증가율']

i = 0 # mid_select 인덱스 초기화

# table 결과 리스트 초기화
table_list=[]

with open(csv_file_name, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(column_list)  # 컬럼 설정

    # 중분류에 따라 반복문 실행
    for value in selIndus_list:

        # chromedriver로 브라우저 실행(정보공개서 브랜드별)
        browser = webdriver.Chrome('/Users/SAMSUNG/chromedriver_win32/chromedriver')
        browser.get('https://franchise.ftc.go.kr/user/extra/main/221/firHope/listHq/jsp/LayOutPage.do')

        # 업종 대분류 설정(21=외식, 22=도소매, 23=서비스)
        selUpjong = Select(browser.find_element_by_id('selUpjong'))
        selUpjong.select_by_value(selUpjong_value)
        time.sleep(1)

        # 업종 중분류 설정
        selIndus = Select(browser.find_element_by_id('selIndus'))
        selIndus.select_by_value(value)
        time.sleep(1)

        # 비교 항목('listBrand01','listBrand02','listBrand03') (브랜드개요, 현황정보, 창업비용)
        selListType = Select(browser.find_element_by_id('selListType'))
        selListType.select_by_value(item)
        time.sleep(1)

        # 검색버튼 클릭
        browser.find_element_by_xpath('//*[@id="frmSearch"]/input[5]').click()
        time.sleep(1)

        # table 크롤링(table -> tbody -> tr -> td)
        table = browser.find_element_by_tag_name('table') # table 지정
        tbody = table.find_element_by_tag_name('tbody') # tbody 지정

        # tr 태그 추출 후 td를 table_list에 저장
        try:
            for tr in tbody.find_elements_by_tag_name('tr'):
                td = tr.find_elements_by_tag_name('td') # 해당 tr에 td 추출

                table_list.append(selUpjong_kor)
                table_list.append(mid_select[i])
                table_list.append(td[0].text)
                table_list.append(td[2].text)
                table_list.append(td[5].text)

                print(table_list) # 잘 추출 되는지 확인
                w.writerow(table_list)  # csv 파일에 저장
                table_list = [] # 다시 table 초기화

        except:
               print('error')

        i += 1 # 중분류(한글명) 인덱스 증가
        # browser 완료되면 종료
        browser.close()

    print('finish')