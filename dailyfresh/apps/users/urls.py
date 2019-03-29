
from . import views
from django.conf.urls import url
from .views import RegisterView, Login, Active_View

urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^login$', Login.as_view(), name='login'),
    url(r'^active/(?P<token>.*)$', Active_View.as_view(), name='active'),
    #url(r'^active/(?P<token>.*)$', Active_View.as_view(), name='active'),
]
