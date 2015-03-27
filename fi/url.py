from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from pf2.fi.models import *
#from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('pf2.fi.views',
    # Examples:
    url(r'^test/(?P<year>\d+)/$','test')

)
