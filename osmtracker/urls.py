from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from follower.views import MapperView
from follower.views import MapperCreateView
from follower.views import EmailCreateView
from follower.views import EmailUpdateView
from follower.views import EmailDeleteView
from follower.views import EmailListView
from follower.views import MapperListView

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import login

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'osmtracker.views.home', name='home'),
    # url(r'^osmtracker/', include('osmtracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
    ,url(r'^accounts/login/$', 'django.contrib.auth.views.login')
    ,url(r'^list/list_action','follower.views.mapper_bulk_action')
    ,url(r'^mapper_update', 'follower.views.update_mappers')                 
    ,url(r'^mapper/list', login_required(MapperListView.as_view()))
    ,url(r'^reach_out/create','follower.views.reach_out_create')
    ,url(r'^mapper/(?P<id>\d+)',login_required(MapperView.as_view()))
    ,url(r'^mapper/create', login_required(MapperCreateView.as_view()))
    ,url(r'^email/create',login_required(EmailCreateView.as_view()))
    ,url(r'^email/(?P<id>\d+)/delete',login_required(EmailDeleteView.as_view()))
    ,url(r'^email/(?P<id>\d+)', login_required(EmailUpdateView.as_view()))
    ,url(r'^email/list', login_required(EmailListView.as_view()))   
    ,url(r'^$', login_required(MapperListView.as_view()))
)
