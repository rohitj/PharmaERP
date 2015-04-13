from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView


urlpatterns = patterns('',
    url(r'^employee/$', 'views.generalclass.newlist', {"classname": "es.models.Employee", }),
    url(r'^employee/new/$', 'views.generalclass.newnew', {"classname": "es.models.Employee", "oneonone_forms":["user", "User"]}, "create_employee"),
    url(r'^employee/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.Employee"}, "view_employee"),
    url(r'^employee/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.Employee"}, "edit_employee"),

    url(r'^bptype/$', 'views.generalclass.newlist', {"classname": "es.models.BPtype", }),
    url(r'^bptype/new/$', 'views.generalclass.newnew', {"classname": "es.models.BPtype"}, "create_bptype"),
    url(r'^bptype/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.BPtype"}, "view_bptype"),
    url(r'^bptype/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.BPtype"}, "edit_bptype"),

    url(r'^bpartner/$', 'views.generalclass.newlist', {"classname": "es.models.BPartner", }),
    url(r'^bpartner/new/$', 'views.generalclass.newnew', {"classname": "es.models.BPartner"}, "create_bpartner"),
    url(r'^bpartner/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.BPartner"}, "view_bpartner"),
    url(r'^bpartner/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.BPartner"}, "edit_bpartner"),

    url(r'^clientdetails/$', 'views.generalclass.newlist', {"classname": "es.models.ClientDetails", }),
    url(r'^clientdetails/new/$', 'views.generalclass.newnew', {"classname": "es.models.ClientDetails"}, "create_clientdetails"),
    url(r'^clientdetails/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.ClientDetails"}, "view_clientdetails"),
    url(r'^clientdetails/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.ClientDetails"}, "edit_clientdetails"),

    url(r'^plant/$', 'views.generalclass.newlist', {"classname": "es.models.Plant", }),
    url(r'^plant/new/$', 'views.generalclass.newnew', {"classname": "es.models.Plant"}, "create_plant"),
    url(r'^plant/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.Plant"}, "view_plant"),
    url(r'^plant/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.Plant"}, "edit_plant"),

    url(r'^depo/$', 'views.generalclass.newlist', {"classname": "es.models.Depo", }),
    url(r'^depo/new/$', 'views.generalclass.newnew', {"classname": "es.models.Depo"}, "create_depo"),
    url(r'^depo/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.Depo"}, "view_depo"),
    url(r'^depo/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.Depo"}, "edit_depo"),

    url(r'^station/$', 'views.generalclass.newlist', {"classname": "es.models.Station", }),
    url(r'^station/new/$', 'views.generalclass.newnew', {"classname": "es.models.Station"}, "create_station"),
    url(r'^station/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.Station"}, "view_station"),
    url(r'^station/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.Station"}, "edit_station"),

#    url(r'^packing/pgroup/(?P<dependent_id>\d*)/$', 'pf.views.generalclass.list', {"classname": "mm.models.Packing", "classname_dependent": "es.models.PGroup"}, "pgroup_dependent"),
    url(r'^pageno/station/(?P<dependent_on_id>\d*)/$', 'views.generalclass.newlist', {"classname": "es.models.Pageno", "dependent_on": ("station", "es.models.Station")}),
    url(r'^pageno/station/(?P<dependent_on_id>\d*)/new/$', 'views.generalclass.newnew', {"classname": "es.models.Pageno", "dependent_on": ("station", "es.models.Station")}, "create_pageno"),
    url(r'^pageno/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.Pageno"}, "view_pageno"),
    url(r'^pageno/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.Pageno"}, "edit_pageno"),

    url(r'^representative/$', 'views.generalclass.newlist', {"classname": "es.models.Representative", }),
    url(r'^representative/new/$', 'views.generalclass.newnew', {"classname": "es.models.Representative"}, "create_representative"),
    url(r'^representative/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.Representative"}, "view_representative"),
    url(r'^representative/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.Representative"}, "edit_representative"),

    url(r'^pagerep/$', 'views.generalclass.newlist', {"classname": "es.models.PageRep", }),
    url(r'^pagerep/new/$', 'views.generalclass.newnew', {"classname": "es.models.PageRep"}, "create_pagerep"),
    url(r'^pagerep/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.PageRep"}, "view_pagerep"),
    url(r'^pagerep/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.PageRep"}, "edit_pagerep"),

    url(r'^salestax/$', 'views.generalclass.newlist', {"classname": "es.models.SalesTax", }),
    url(r'^salestax/new/$', 'views.generalclass.newnew', {"classname": "es.models.SalesTax"}, "create_salestax"),
    url(r'^salestax/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.SalesTax"}, "view_salestax"),
    url(r'^salestax/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.SalesTax"}, "edit_salestax"),


)
