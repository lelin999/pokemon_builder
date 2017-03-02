from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^/stat_ajax/?$', views.stat_ajax),
]
