from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
from login import get_user

URL = "https://nid.naver.com/nidlogin.login"
DRIVER_DIR = 'C:/Users/dkdud/Desktop/fastcampus/chromedriver'

ID, PW = get_user()

def naver_scrap():
    try:
        driver = webdriver.Chrome(DRIVER_DIR)
        driver.implicitly_wait(10)
        driver.get(URL)
        print("로그인 페이지에 접근")

        e = driver.find_element_by_id("id")
        # input 태그를 지워줌
        e.clear()
        # 본인의 ID를 로그인 창에 넣어줌
        e.send_keys(ID)

        e = driver.find_element_by_id("pw")
        e.clear()
        e.send_keys(PW)
        
        form = driver.find_element_by_css_selector("input.btn_global[type=submit]")
        form.submit()
        print("로그인 버튼을 클릭")

        # BASE 시작 유랑 여행후기 게시판
        # 개발자 도구에서 클릭하고 새로운 창의 url 복사
        driver.get('https://cafe.naver.com/firenze?iframe_url=/ArticleList.nhn%3Fsearch.clubid=10209062%26search.menuid=59%26search.boardtype=L%26search.totalCount=151%26search.page=1')
        # iframe 값
        driver.switch_to.frame('cafe_main')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        BASE = 'https://cafe.naver.com/'
        spans = []
        # link 주소
        # soup.select는 find_element_by_css_seletor와 비슷한 역할
        for span_tag in soup.select('table.board-box > tbody span.aaa'):
            spans.append(BASE + str(span_tag.find('a')['href']))
            break

        # 글쓴이와 댓글 가져오기
        for idx, span in enumerate(spans):
            driver.get(span) # 하나의 페이지
            driver.switch_to.frame('cafe_main') # iframe 가져오기
            html = driver.page_source # 페이지 소스 가져오기
            soup = BeautifulSoup(html, 'html.parser') # 페이지 소스 html 코드로 파싱

            t = soup.select('div#main-area div.inbox')[0] # 본문 내용 가져오기
            author = t.select('div.fl td.p-nick a')[0].get_text() # 글쓴이
            print('(글쓴이)-> ', author)

            cmt_list = t.find('ul', attrs={'id':'cmt_list'}) # 댓글목록
            for com in cmt_list.select('li'):
                user = com.find('a', attrs={'class' : '_nickUI'}) # 댓글 작성자
                date = com.find('span', attrs={'class', 'date'})
                comm = com.find('span', attrs={'class', 'comm_body'}) # 작성 글
                if user is not None: # 사용자가 있다면
                    print(user.get_text(), date.get_text(), comm.get_text())

    except Exception as e:
        print(e)
    finally:
        driver.close()

if __name__ == "__main__":
    naver_scrap()





