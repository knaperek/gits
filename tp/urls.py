from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^exam/', include('exam.urls', namespace='exam')),
    # Examples:
    # url(r'^$', 'tp.views.home', name='home'),
    # url(r'^tp/', include('tp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^$', lambda request: TemplateView.as_view(template_name='index.html')(request)),
    url(r'^$', TemplateView.as_view(template_name='user/index.html')),
	url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='accounts-logout'),
    url(r'^accounts/password_change/$', 'django.contrib.auth.views.password_change', name='accounts-password-change'),
    url(r'^accounts/password_change_done/$', 'django.contrib.auth.views.password_change_done'),
    url(r'^accounts/$', RedirectView.as_view(url='/exam')),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns
