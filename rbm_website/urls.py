from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'rbm_website.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/$', 'rbm_website.views.admin', name='admin'),
    url(r'^about/$', 'rbm_website.views.about', name='about'),
    url(r'^rbm/', include('rbm_website.apps.rbm.urls')),
    url(r'^users/', include('rbm_website.apps.users.urls')),
    url(r'^accounts/logout/', 'rbm_website.apps.users.views.user_logout'),
    url(r'^accounts/', include('registration.backends.simple.urls'))


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)
