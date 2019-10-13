import time
from selenium import webdriver

URL = "https://twitter.com/search?q={}&src=typd"
DRIVER_DIR = 'C:/Users/dkdud/Desktop/fastcampus/chromedriver'

def twitter(keyword):
    driver = webdriver.Chrome(DRIVER_DIR)
    driver.implicitly_wait(10)
    driver.get(URL.format(str(keyword)))
    try:
        # 스크롤링 되게
        no_page = 0
        while no_page < 10:
            # 자바스크립트에서 x값이 0, y값이 body.scrollHeight가 되게 (높이만큼 전부 scrolling)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            no_page += 1
            time.sleep(1.5)

        # 모든 트윗 리스트
        content = driver.find_elements_by_css_selector('div.content')
        print("content-length: ", len(content))
        # 반복문으로 각각의 트윗 뽑아오기
        for i in content:
            # 트윗 텍스트
            cont = i.find_elements_by_css_selector('p.tweet-text')[0]
            # 트윗 업로드 시간
            timestamp = i.find_elements_by_css_selector('a.tweet-timestamp')[0]
            print(str(cont.text), timestamp.get_attribute("title"))
            print('---------------------------------------')

    except Exception as e:
        print(e)
    finally:
        driver.close()

if __name__ == "__main__":
    keyword = input('keyword?')
    twitter(str(keyword))
