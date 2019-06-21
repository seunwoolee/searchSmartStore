from django.contrib import admin
from django.urls import path, include

from api.views import Item
from search import views

urlpatterns = [
    path('detail/<int:pk>', Item.as_view()),
]
