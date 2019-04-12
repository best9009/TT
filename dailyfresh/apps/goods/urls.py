"""TianTianFrush URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from .views import Index, DetailView, ListView

urlpatterns = [
    url(r'^index$', Index.as_view(), name='index'),
    url(r'^detail/(?P<goods_id>\d+)$', DetailView.as_view(), name='detail'),
    #列表详情传递三个参数 type:商品种类 page对象 sort排序方式/list/1/1?sort=''
    url(r'^list/(?P<type_id>\d+)/(?P<page_num>\d+)$', ListView.as_view(), name='list'),
]
