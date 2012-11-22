from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'osmtracker.views.home', name='home'),
    # url(r'^osmtracker/', include('osmtracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
    ,url(r'^list/list_action','follower.views.mapper_bulk_action')
    ,url(r'^list', 'follower.views.list')                 
    ,url(r'^reach_out/create','follower.views.reach_out_create')
)
