from django.contrib import admin
from .models import Log, Items, ProductCode, RankItem


# Register your models here

@admin.register(Log, Items, ProductCode, RankItem)
class DefaultAdmin(admin.ModelAdmin):
    pass
