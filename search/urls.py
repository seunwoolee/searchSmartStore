from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from search import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.MainList.as_view(), name='index'),
    path('', include('pwa.urls')),
    path('detail/', views.Detail.as_view(), name='detail'),
    path('api/', include('api.urls')),
]
