from django.conf.urls import patterns, include, url
from rbm_website.apps.rbm import views

urlpatterns = patterns('',
        url(r'^$', views.RBMListView.as_view(), name='index'),
        url(r'^create/$', views.create, name='create'),
        url(r'^(?P<pk>\d+)/$', views.RBMDetailView.as_view(), name='view'),
        url(r'^(?P<rbm_id>\d+)/regenerate/$', views.regenerate, name='regenerate'),
        url(r'^(?P<rbm_id>\d+)/train/$', views.train, name='train'),
        url(r'^training/$', views.training, name='training')
        )
