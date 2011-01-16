from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
import django.contrib.auth
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'future_todo.views.index', name="index"),
    
    (r'^accounts/', include('django.contrib.auth.urls')),
    
    (r'^schedule/', include('schedule.urls')),
    (r'^todo/', include('todo.urls')),
    (r'^ajax/', 'future_todo.views.ajax'),
    
    url(r'^task_add', 'future_todo.views.task_add', name="task_add"),
    url(r'^plugins/list/(?P<list_id>\d{1,4})/run', 'future_todo.views.list_run', name="list_run"),
    url(r'^plugins', 'future_todo.views.plugins', name="plugins"),


    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/todo/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.TODO_MEDIA_ROOT+'/todo/', 'show_indexes': True}),

        (r'^site_media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
         
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.TODO_MEDIA_ROOT, 'show_indexes': True}),

    )

