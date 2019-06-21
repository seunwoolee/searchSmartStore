from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.itemSerializers import ItemsSerializer
from log.models import Items, ProductCode, RankItem
import datetime

class Item(APIView):
    """
    아이템 분석 - TD 클릭 시 json 반환
    """

    def get(self, request, pk):
        result = {}
        new_format = '%Y-%m-%d %H:%M:%S'
        product_code = ProductCode.objects.get(pk=pk)
        items: Items = Items.objects.filter(product_code=product_code)
        keywords = [item.result_product_log for item in items if item.result_product_log]

        for keyword in keywords:
            keyword_items = Items.objects.filter(product_code=product_code).filter(result_product_log=keyword)
            for keyword_item in keyword_items:
                hash_value = []
                hash_key = f'{keyword_item.product_code.product_name}_{keyword_item.result_product_log.keywords}'
                ranking_number = []
                ranking_time = []

                for rankItem in RankItem.objects.filter(item=keyword_item):
                    if rankItem:
                        ranking_number.append(rankItem.ranking_number)
                        ranking_time.append(rankItem.created.strftime(new_format))

                hash_value.append(ranking_number)
                hash_value.append(ranking_time)

                result[hash_key] = hash_value

        return Response(result, status=status.HTTP_200_OK)