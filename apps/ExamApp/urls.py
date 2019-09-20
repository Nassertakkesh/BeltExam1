from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^wishes$', views.presuccess),
    url(r'^wishes/new$', views.makewishhtml),
    url(r'^wishes/newitem$', views.makewish),
    url(r'^wishes/edit/(?P<id>\d+)$', views.editwishhtml),
    url(r'^wishes/edititem/(?P<id>\d+)$', views.editwish),
    url(r'^wishes/delete/(?P<id>\d+)$', views.delete),
    url(r'^wishes/granted/(?P<id>\d+)$', views.granted),
    url(r'^wishes/stats$', views.stats),
     url(r'^wishes/like/(?P<id>\d+)$', views.like),



]

