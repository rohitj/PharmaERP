from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('',
    # Examples:
    url(r'^customer/$', 'views.generalclass.newlist', {"classname": "sd.models.Customer", }),
    url(r'^customer/new/$', 'views.generalclass.newnew', {"classname": "sd.models.Customer"}, "create_customer"),
    url(r'^customer/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "sd.models.Customer"}, "view_customer"),
    url(r'^customer/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "sd.models.Customer"}, "edit_customer"),

)
