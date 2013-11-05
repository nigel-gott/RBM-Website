from django.conf.urls import patterns, include, url
from rbm_website.apps.rbm import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index')
        )
