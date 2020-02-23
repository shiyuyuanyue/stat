from django.conf.urls import url
from tools import views

urlpatterns = [
    url(r'^$',views.makedatas),
    url(r'^/make_score$',views.make_score),
]