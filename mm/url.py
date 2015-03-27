from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from pf2.es.models import *
#from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('pf2.mm.views',
    # Examples:
    url(r'^test/(?P<year>\d+)/$','test'),
    url(r'^admin/', include(admin.site.urls))
)
