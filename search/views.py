from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from log.models import Log
from search.forms import SearchForm


@method_decorator(csrf_exempt, name='dispatch')
class MainList(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.company_name: str = ''
        self.keywords: str = ''
        self.naver_shopping_url: str = 'https://shopping.naver.com/'
        self.driver:webdriver = webdriver.Chrome('chromedriver')
        self.result: list = []


    def get(self, request):
        form = SearchForm()
        return render(request, 'index.html', {'form': form})

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            self.company_name: str = form.cleaned_data['company_name']
            self.keywords: str = form.cleaned_data['keywords']
            self.search_keywords()

        form = SearchForm()
        return render(request, 'index.html', {'form': form})

    def search_keywords(self) -> dict:
        self.driver.get(self.naver_shopping_url)
        self.driver.find_element_by_name('query').send_keys(self.keywords)
        self.driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/a[2]').click()
        html:str = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        product_info: BeautifulSoup = soup.select('div.info')
        seller_info: BeautifulSoup = soup.select('div.info_mall a.mall_img')

        for i, seller in enumerate(seller_info):
            print(self.company_name, seller_info[i].text)
            if self.company_name in seller_info[i].text:
                print('있다')
            else:
                print('없다')

        self.driver.quit()
