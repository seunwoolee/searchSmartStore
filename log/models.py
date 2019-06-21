from django.db import models


class TimeStampedModel(models.Model):
    """
    created , modified filed를 제공해주는 abstract base class model
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Log(TimeStampedModel):
    yn_choices = (
        ('Y', 'Y'),
        ('N', 'N'),
    )
    company_name = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    auto_search = models.CharField(
        max_length=10,
        choices=yn_choices,
        default='N',
    )

    def __str__(self):
        return f'{self.keywords}'


class Items(TimeStampedModel):
    product_code = models.ForeignKey('ProductCode', on_delete=models.CASCADE, null=True, blank=True)
    result_product_name = models.CharField(max_length=255)
    result_product_price = models.CharField(max_length=255)
    result_product_category = models.CharField(max_length=255)
    result_product_ranking = models.CharField(max_length=255)
    result_product_ranking_number = models.IntegerField()
    result_product_log = models.ForeignKey('Log', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'상품명: {self.result_product_name} 키워드: {self.result_product_log}'


class ProductCode(TimeStampedModel):
    company_name = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.company_name}{self.product_name}'


class RankItem(TimeStampedModel):
    item = models.ForeignKey('Items', on_delete=models.CASCADE, null=True, blank=True)
    ranking = models.CharField(max_length=255)
    ranking_number = models.IntegerField()
    ranking_diff = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.item}'
        # if self.ranking_diff < 0:
        #     return f' 키워드: {self.item.result_product_log.keywords} 정보: {self.item.__str__} 현재순위: {self.ranking} '
        # else:
        #     return f'{self.ranking_diff} 순위상승 (^_^) 키워드: {self.item.result_product_log.keywords} 상품명 : {self.item.result_product_name} 현재순위: {self.ranking}'
