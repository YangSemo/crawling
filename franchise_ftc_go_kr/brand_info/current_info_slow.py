from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import csv
from openpyxl import Workbook, load_workbook

# chromedriver로 브라우저 실행(정보공개서 브랜드별)
browser = webdriver.Chrome('/Users/SAMSUNG/chromedriver_win32/chromedriver')
browser.get('https://franchise.ftc.go.kr/user/extra/main/70/firHope/listBrand/jsp/LayOutPage.do/')

# 업종 대분류('21','22','23')
selUpjong = Select(browser.find_element_by_id('selUpjong'))
selUpjong.select_by_value('21')
time.sleep(1)

# 업종 중분류('A1','B1','C1','D1','E1','F1','G1','H1','I1','K1','L1','M1','N1','01')
selIndus = Select(browser.find_element_by_id('selIndus'))
selIndus.select_by_value('B1')
time.sleep(1)

# 비교 항목('listBrand01','listBrand02','listBrand03')
selListType = Select(browser.find_element_by_id('selListType'))
selListType.select_by_value('listBrand02')
time.sleep(1)

# 검색버튼 클릭
browser.find_element_by_xpath('//*[@id="frmSearch"]/input[5]').click()
time.sleep(1)


# table 결과 리스트
table_list=[]


# table 크롤링
table = browser.find_element_by_tag_name('table')
tbody = table.find_element_by_tag_name('tbody')
trs = tbody.find_elements_by_tag_name('tr')



# csv 파일로 저장
column_list = ['브랜드','상호','가맹점수','신규개점','계약종료','계약해지','명의변경','가맹점평균매출액(매출액지수)','가맹점면적당평균매출액']

with open('brand_info_분.csv','w',encoding='utf-8-sig',newline='') as f:
    w = csv.writer(f)
    w.writerow(column_list)

    for td in trs:
        td_text = td.text
        td_list = td_text.split(' ')
        print(td_list)
        w.writerow(td_list)

    browser.close()
    print('finish')