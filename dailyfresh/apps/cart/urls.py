
from .views import AddCartView, CartView, CartUpdateView, CartDelView
from django.conf.urls import url

urlpatterns = [
    url(r'^add$', AddCartView.as_view(), name='add'),
    url(r'^$', CartView.as_view(), name='info'),
    url(r'^update$', CartUpdateView.as_view(), name='update'),
    url(r'^del', CartDelView.as_view(), name='del')
]