import django
from django.http import JsonResponse
from django.template.loader import render_to_string

django.setup()
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from bs4 import BeautifulSoup
import requests
import time

from log.models import Log
from search.forms import SearchForm
import requests

from multiprocessing import Pool, Process


def search_urls(url):  # class안에 넣으면 시리얼 에러남
    req = requests.get(url)
    html = req.text
    return html


@method_decorator(csrf_exempt, name='dispatch')
class MainList(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.company_name: str = ''
        self.keywords: str = ''
        self.naver_shopping_url: str = ''
        self.urls: list = []
        self.result: list = []
        self.pool: Pool = Pool(processes=4)
        self.search_urls = search_urls
        self.htmls: list = []

    def get(self, request):
        form = SearchForm()
        return render(request, 'index.html', {'form': form})

    def post(self, request):
        data: dict = dict()
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            self.company_name: str = form.cleaned_data['company_name']
            self.keywords: str = form.cleaned_data['keywords']
            self.get_links()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        # logs = Log.objects.all()
        logs = [{'id': 1, 'company_name': '승우', 'keywords': '짱'}]
        data['html_ranking_list'] = render_to_string('partial_ranking_list.html', {'logs': logs})
        return JsonResponse(data)

    def get_links(self):
        for i in range(1, 11):
            self.naver_shopping_url = f'https://search.shopping.naver.com/search/all.nhn?origQuery={self.keywords}&pagingIndex={i}' \
                f'&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={self.keywords}'
            self.urls.append(self.naver_shopping_url)
        self.htmls: list = self.pool.map(self.search_urls, self.urls)
        self.check_items()
        # self.pool.map(self.check_items, htmls)

    def check_items(self) -> list:

        for i, html in enumerate(self.htmls):
            soup = BeautifulSoup(html, 'html.parser')
            # product_info: BeautifulSoup = soup.select('ul.goods_list div.info')
            product_name: BeautifulSoup = soup.select('ul.goods_list div.info a.tit')
            product_price: BeautifulSoup = soup.select('ul.goods_list div.info span.price em')
            product_advertise: BeautifulSoup = soup.select('ul.goods_list div.info span.price a.ad_stk')
            product_categorys: BeautifulSoup = soup.select('ul.goods_list div.info span.depth a')
            seller_info: BeautifulSoup = soup.select('ul.goods_list div.info_mall a.mall_img')

            for j, seller in enumerate(seller_info):
                clean_company_name: str = seller_info[j].text
                clean_product_name: str = product_name[j].text.strip()
                clean_product_price: str = product_price[j].text.strip()

                try:
                    clean_product_advertise: str = f'({product_advertise[i].text.strip()})'
                except:
                    clean_product_advertise: str = ''

                if self.company_name in clean_company_name:
                    test = []
                    for product_category in product_categorys:
                        test.append(product_category.text.strip())
                        print(test)
                        print('####')

                    result_product_name = f'{clean_product_name}{clean_product_advertise}'
                    result_company_name = self.company_name
                    result_ranking = f'{i+1}페이지 {j+1}위'
                    result_price = clean_product_price
                    print(f'{i+1}페이지 {j+1}위 {result_product_name} {clean_product_price}')