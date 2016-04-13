from django.conf.urls import url
from . import views

urlpatterns = [
    # /order/
    url(r'^$', views.index, name='index'),
]