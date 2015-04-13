from django.conf.urls import patterns, include, url
from django.contrib import admin
import os
from django.conf import settings


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PharmaERP.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.BASE_DIR, 'site_media')}),
    url(r'^$', 'views.views.run'),


    url(r'^es/', include("es.url")),
    url(r'^mm/', include("mm.url")),
    url(r'^sd/', include("sd.url")),
    url(r'^pp/', include("pp.url")),

)
