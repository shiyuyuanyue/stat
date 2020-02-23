from django.conf.urls import url

from stoken import views

urlpatterns = [
    url('^$',views.stoken)
]