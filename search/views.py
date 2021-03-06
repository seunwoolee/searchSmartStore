import django
from django.http import JsonResponse
from django.template.loader import render_to_string

django.setup()
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from bs4 import BeautifulSoup
from log.models import Log, Items, ProductCode, RankItem
from search.forms import SearchForm
import requests

from multiprocessing import Pool, Process

import telegram

TOKEN = '865080373:AAFuVoSdoIrrWHxpe0ny9_LumSUrrbrS_S8'


def search_urls(url):  # class안에 넣으면 시리얼 에러남
    req = requests.get(url)
    html = req.text
    return html


@method_decorator(csrf_exempt, name='dispatch')
class MainList(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.company_name: str
        self.keywords: str
        self.product_name: str
        self.naver_shopping_url: str
        self.urls: list = []
        self.result: list = []
        self.pool: Pool = Pool(processes=4)
        self.search_urls = search_urls
        self.htmls: list = []
        self.log: Log

    def get(self, request):
        form = SearchForm()
        return render(request, 'index.html', {'form': form})

    def post(self, request):
        data: dict = dict()
        form = SearchForm(request.POST)
        if form.is_valid():
            self.company_name: str = form.cleaned_data['company_name']
            self.keywords: str = form.cleaned_data['keywords']
            self.log = Log.objects.filter(company_name=self.company_name).filter(keywords=self.keywords).first()

            if not self.log:
                form.save()

            self.get_links()
            self.check_items()

            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        data['html_ranking_list'] = render_to_string('partial_ranking_list.html', {'results': self.result})
        return JsonResponse(data)

    def get_links(self):
        for i in range(1, 11):
            self.naver_shopping_url = f'https://search.shopping.naver.com/search/all.nhn?origQuery={self.keywords}&pagingIndex={i}' \
                f'&pagingSize=40&viewType=list&sort=rel&frm=NVSHPAG&query={self.keywords}'
            self.urls.append(self.naver_shopping_url)
        self.htmls: list = self.pool.map(self.search_urls, self.urls)

    def check_items(self):
        for i, html in enumerate(self.htmls):
            soup = BeautifulSoup(html, 'html.parser')
            product_name: list = soup.select('ul.goods_list div.info a.tit')
            product_price: list = soup.select('ul.goods_list div.info span.price em')
            product_advertise: list = soup.select('ul.goods_list div.info span.price a.ad_stk')
            product_categorys: list = soup.select('ul.goods_list div.info span.depth a')
            seller_info: list = soup.select('ul.goods_list div.info_mall a.mall_img')

            for j, seller in enumerate(seller_info):
                clean_company_name: str = seller_info[j].text
                clean_product_name: str = product_name[j].text.strip()
                clean_product_price: str = product_price[j].text.strip()

                try:
                    clean_product_advertise: str = f'({product_advertise[j].text.strip()})'
                except:
                    clean_product_advertise: str = ''

                if clean_company_name == '쇼핑몰별 최저가':
                    cheap_seller_list: list = soup.select('ul.goods_list li:nth-child('+str(j+1)+') div.info_mall ul.mall_list')
                    clean_cheap_seller_list: str = cheap_seller_list[0].text.strip()
                else:
                    clean_cheap_seller_list: str = ''

                if self.company_name in clean_company_name or self.company_name in clean_cheap_seller_list:
                    product_category: BeautifulSoup = product_categorys[-1]
                    result_product_category: str = f'{product_category.get("title")} > {product_category.text}'
                    result_product_name: str = f'{clean_product_name}{clean_product_advertise}'
                    self.product_name = result_product_name
                    result_product_ranking: str = f'{i + 1}페이지 {j + 1}위'
                    result_product_ranking_number: int = i * 40 + j
                    result_product_price: str = clean_product_price

                    result: dict = dict(result_product_name=result_product_name,
                                        result_product_price=result_product_price,
                                        result_product_category=result_product_category,
                                        result_product_ranking=result_product_ranking,
                                        result_product_ranking_number=result_product_ranking_number,
                                        result_product_log=self.log)

                    self.create_item(result)

                    result['result_company_name'] = self.company_name
                    self.result.append(result)
                    print(f'키워드: {self.keywords} {i + 1}페이지 {j + 1}위 {result_product_name} {result_product_price} ')

    def create_item(self, dict):
        product_code: ProductCode = ProductCode.objects.filter(company_name=self.company_name) \
            .filter(product_name=self.product_name).first()
        item: Items = Items.objects.filter(product_code=product_code).filter(result_product_log=self.log).first()
        if not product_code:
            product_code = ProductCode(company_name=self.company_name, product_name=self.product_name)
            dict['product_code'] = product_code
            product_code.save()
            Items(**dict).save()
        elif not item:
            dict['product_code'] = product_code
            Items(**dict).save()
        else:  # 기존에 item이 있으면 랭킹 Insert
            last_rank_item: RankItem = RankItem.objects.filter(item=item).last()

            if last_rank_item:
                origin_ranking: int = last_rank_item.ranking_number
            else:
                origin_ranking: int = item.result_product_ranking_number

            ranking_diff = origin_ranking - dict['result_product_ranking_number']

            if ranking_diff != 0:
                rankitem = RankItem(item=item,
                                    ranking=dict['result_product_ranking'],
                                    ranking_number=dict['result_product_ranking_number'],
                                    ranking_diff=ranking_diff)
                rankitem.save()

                if last_rank_item:
                    message = f' {last_rank_item.__str__()} (순위: {last_rank_item.ranking}-> {rankitem.ranking} {ranking_diff}) '
                else:
                    message = f' {item.__str__()} (순위: {item.result_product_ranking}-> {rankitem.ranking} {ranking_diff}) '

                if '광고' in item.result_product_name and item.result_product_ranking_number < 60:
                    self.send_message(message)

    def send_message(self, text):
        global TOKEN
        bot: telegram = telegram.Bot(token=TOKEN)
        chat_id = '826706369'
        bot.sendMessage(chat_id=chat_id, text=text)


class Detail(View):

    def get(self, request):
        product_codes = ProductCode.objects.all()
        return render(request, 'detail.html', {'product_codes': product_codes})
