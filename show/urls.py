from django.conf.urls import url
from show import views

urlpatterns = [
    url(r'^$',views.search_api)
]