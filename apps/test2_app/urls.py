from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), #this is my dashbord page
    url(r'^add$', views.add),
    url(r'^create$', views.create),
    url(r'^userpage/(?P<id>\d+)$', views.userpage),
    url(r'^delete/(?P<id>\d+)$', views.delete),

]