from django.conf.urls import *
from django.conf import settings
from pf2.pp.models import *
from pf2.es.models import *
from django.views.generic import DetailView, ListView

urlpatterns = patterns('',
    url(r'^distt/new/(\d+)/$', 'pf2.pp.views.newdistt'),
    url(r'^rmarea/$',ListView.as_view(queryset=Rmarea.objects.all(),
                                 context_object_name='rmarea_list',
                                 template_name='rmarea_list.html')),
    url(r'^mbatch/$',ListView.as_view(queryset=Rmarea.objects.all(),
                                 context_object_name='rmarea_list',
                                 template_name='mbatch_list.html')),
    url(r'^newfs/ajax/$','pf2.pp.views.xhr_test'),
    url(r'^newfs/$','pf2.pp.views.newfs1'),
    url(r'^newbatch/$','pf2.pp.views.newbatch'),
    url(r'^changebatch/distt/$','pf2.pp.views.newdistt2'),
    url(r'^changebatch/save/$','pf2.pp.views.changebatch'),
    url(r'^changebatch/(\d+)/$','pf2.pp.views.changebatch'),
    url(r'^newbatch/prod/$','pf2.pp.views.prod'),
    url(r'^newbatch/save/$','pf2.pp.views.newbatch'),
    url(r'^newbatch/distt/$','pf2.pp.views.newdistt2'),
    url(r'^batchlist/$','pf2.pp.views.batchlist'),
    url(r'^batchlist/ajax/$','pf2.pp.views.xhr_test'),
    url(r'^newfs/ajax/$', 'pf2.pp.views.xhr_test1'),
    url(r'^ajax1/$', 'pf2.pp.views.batchlist1')
)
