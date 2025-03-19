import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from threading import Thread

# Selenium으로 크롤링한 기사 제목과 링크를 가져오는 함수
def get_articles():
    URL = 'https://news.naver.com/breakingnews/section/103/241'
    driver = webdriver.Chrome()
    driver.get(URL)

    articles = []
    
    
    def click_more_button():#기사 더보기 버튼 클릭 및 기사 목록 크롤링
        try:
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#newsct > div.section_latest > div > div.section_more > a.section_more_inner'))
            )
            element.click()
        except:
            print("더 이상 기사 더보기 버튼이 없습니다.")
    
    num = 4  #더보기 버튼 클릭 횟수
    for i in range(num):  #num번 더보기 클릭 (6개씩 기사 추가)
        click_more_button()
        time.sleep(2)

    # 크롤링한 기사 제목과 링크 수집
    for i in range(1, num * 6 + 1):  #num*6개의 기사를 가져오기
        try:
            title_element = driver.find_element(By.CSS_SELECTOR, f'#newsct > div.section_latest > div > div.section_latest_article._CONTENT_LIST._PERSIST_META > div:nth-child({i}) > ul > li:nth-child(1) > div > div > div.sa_text > a')
            title = title_element.text
            link = title_element.get_attribute("href")
            articles.append((title, link))
        except Exception as e:
            print(f"Error: {e}")
            break

    driver.quit()
    return articles

