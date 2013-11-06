from django.conf.urls import patterns, include, url
from rbm_website.apps.rbm import views

urlpatterns = patterns('',
        url(r'^$', views.RBMList.as_view(), name='index'),
        url(r'^create/$', views.create, name='create'),
        url(r'^(?P<rbm_id>\d+)/$', views.view, name='view'),
        url(r'^(?P<rbm_id>\d+)/regenerate/$', views.regenerate, name='regenerate')
        )
