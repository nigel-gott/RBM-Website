from django.conf.urls import patterns, include, url
from rbm_website.apps.rbm import views

urlpatterns = patterns('',
    url(r'^$', views.dbn_list, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<pk>\d+)/$', views.DBNDetailView.as_view(), name='view'),
    url(r'^(?P<dbn_id>\d+)/train/$', views.train, name='train'),
    url(r'^(?P<dbn_id>\d+)/delete/$', views.delete, name='delete'),
    url(r'^training/$', views.training, name='training'),
    url(r'^(?P<dbn_id>\d+)/classify/$', views.classify, name='classify')
)
