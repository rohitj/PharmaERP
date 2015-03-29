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


    url(r'^employee/$', 'views.generalclass.list', {"classname": "es.models.Employee", "classname_nested":"django.contrib.auth.models.User"}),
    url(r'^employee/new/$', 'views.generalclass.new', {"classname": "es.models.Employee", "classname_nested":"django.contrib.auth.models.User"}, "create_employee"),
    url(r'^employee/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.Employee"}, "view_employee"),
    url(r'^employee/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.Employee"}, "edit_employee"),

    url(r'^client/$', 'views.generalclass.list', {"classname": "es.models.Clt"}),
    url(r'^client/new/$', 'views.generalclass.new', {"classname": "es.models.Clt"}, "create_client"),
    url(r'^client/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.Clt"}, "view_client"),
    url(r'^client/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.Clt"}, "edit_client"),


    url(r'^plant/$', 'views.generalclass.list', {"classname": "es.models.Rmarea"}),
    url(r'^plant/new/$', 'views.generalclass.new', {"classname": "es.models.Rmarea"}, "create_plant"),
    url(r'^plant/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.Rmarea"}, "view_plant"),
    url(r'^plant/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.Rmarea"}, "edit_plant"),


    url(r'^pgroup/$', 'views.generalclass.list', {"classname": "mm.models.Pgroup"}),
    url(r'^pgroup/new/$', 'views.generalclass.new', {"classname": "mm.models.Pgroup"}, "create_pgroup"),
    url(r'^pgroup/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "mm.models.Pgroup"}, "view_pgroup"),
    url(r'^pgroup/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "mm.models.Pgroup"}, "edit_pgroup"),


    url(r'^packing/pgroup/(?P<dependent_id>\d*)/$', 'views.generalclass.list', {"classname": "mm.models.Packing", "classname_dependent": "mm.models.Pgroup"}, "pgroup_dependent"),
    url(r'^packing/new/$', 'views.generalclass.new', {"classname": "mm.models.Packing"}, "create_packing"),
    url(r'^packing/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "mm.models.Packing"}, "edit_packing"),
    url(r'^packing/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "mm.models.Packing"}, "view_packing"),


    url(r'^rmrecipe/pgroup/(?P<dependent_id>\d*)/$', 'views.generalclass.edit', {"classname": "pp.models.Rmrecipemaster", "classname_nested": "pp.models.Rmrecipe", "classname_dependent": "es.models.PGroup"}, "rmrecipe_dependent"),
    url(r'^rmrecipe/new/$', 'views.generalclass.new', {"classname": "mm.models.Rmrecipemaster"}, "create_rmrecipemaster"),
    url(r'^rmrecipe/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "mm.models.Rmrecipemaster"}, "edit_rmrecipemaster"),
    url(r'^rmrecipe/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "mm.models.Rmrecipemaster"}, "view_rmrecipemaster"),


    url(r'^rgroup/$', 'views.generalclass.list', {"classname": "mm.models.Rgroup"}),
    url(r'^rgroup/new/$', 'views.generalclass.new', {"classname": "mm.models.Rgroup"}, "create_rgroup"),
    url(r'^rgroup/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "mm.models.Rgroup"}, "view_rgroup"),
    url(r'^rgroup/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "mm.models.Rgroup"}, "edit_rgroup"),


    url(r'^rcode/rgroup/(?P<dependent_id>\d*)/$', 'views.generalclass.list', {"classname": "mm.models.Rcode", "classname_dependent": "mm.models.Rgroup"}, "rgroup_dependent"),
    url(r'^rcode/new/$', 'views.generalclass.new', {"classname": "mm.models.Rcodeas"}, "create_rcode"),
    url(r'^rcode/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "mm.models.Rcodeas"}, "edit_rcode"),
    url(r'^rcode/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "mm.models.Rcodeas"}, "view_rcode"),

)
