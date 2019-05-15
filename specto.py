from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "search.settings")
django.setup()


if __name__ == '__main__':
    naver_shopping_url = 'https://shopping.naver.com/'
    driver = webdriver.Chrome('chromedriver')
    driver.get(naver_shopping_url)

    driver.find_element_by_name('query').send_keys('유아헤어핀')
    driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/a[2]').click()
    driver.quit()

    driver.implicitly_wait(5)

    driver.get('http://118.34.86.119:9092/Data/Groups/')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(('className', 'standartTreeRow'))
    )
    driver.execute_script("document.getElementsByClassName('standartTreeRow')[4].click()")

    time.sleep(2)

    html = driver.execute_script("return document.getElementsByClassName('obj row20px')[0].innerHTML")
    soup = BeautifulSoup(html, 'html.parser')
    td = soup.select("tbody tr td")