
from django.conf.urls import url
from .views import RegisterView, Login, Active_View, User_Center, User_Order, User_Site, User_Logout

urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^login$', Login.as_view(), name='login'),
    url(r'^active/(?P<token>.*)$', Active_View.as_view(), name='active'),
    #url(r'^active/(?P<token>.*)$', Active_View.as_view(), name='active'),
    url(r'^user$', User_Center.as_view(), name='user'),
    url(r'^order/(?P<page_num>\d+)$', User_Order.as_view(), name='order'),
    url(r'^site$', User_Site.as_view(), name='site'),
    url(r'^logout$', User_Logout.as_view(), name='logout'),
]
