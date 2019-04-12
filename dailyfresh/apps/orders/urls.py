from django.conf.urls import  url
from .views import OrderPayView, OrderCommitView

urlpatterns = [
    url(r'^pay$', OrderPayView.as_view(), name='pay'),
    url(r'^commit$', OrderCommitView.as_view(), name='commit')
]