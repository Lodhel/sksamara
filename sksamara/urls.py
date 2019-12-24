from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from filebrowser.sites import site
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('accounts.urls')),

    url(r'^client.php', 'sksamara.views.client', name='client'),
    url(r'^request_technological_accession.php', 'sksamara.views.connection_request', name='connection-request'),
    url(r'^request_technological_accession_success.php', 'sksamara.views.connection_request_success', name='connection-request-success'),
    url(r'^(?P<slug>[-\w\d]+).php', 'sksamara.views.page', name='page'),
    url(r'^$', 'sksamara.views.page', name='page'),

)


from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
