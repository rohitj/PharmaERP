from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('',
    # Examples:
    url(r'^supplier/$', 'views.generalclass.newlist', {"classname": "es.models.Supplier", }),
    url(r'^supplier/new/$', 'views.generalclass.newnew', {"classname": "es.models.Supplier"}, "create_supplier"),
    url(r'^supplier/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "es.models.Supplier"}, "view_supplier"),
    url(r'^supplier/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "es.models.Supplier"}, "edit_supplier"),

    url(r'^pgroup/$', 'views.generalclass.newlist', {"classname": "mm.models.PGroup"}),
    url(r'^pgroup/new/$', 'views.generalclass.newnew', {"classname": "mm.models.PGroup"}, "create_pgroup"),
    url(r'^pgroup/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "mm.models.PGroup"}, "view_pgroup"),
    url(r'^pgroup/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "mm.models.PGroup"}, "edit_pgroup"),

    url(r'^packing/pgroup/(?P<dependent_on_id>\d*)/$', 'views.generalclass.newlist', {"classname": "mm.models.Packing", "dependent_on": ["pgroup", "mm.models.PGroup"]}, ),
    url(r'^packing/pgroup/(?P<dependent_on_id>\d*)/new/$', 'views.generalclass.newnew', {"classname": "mm.models.Packing", "dependent_on": ["pgroup", "mm.models.PGroup"]}, "create_packing"),
    url(r'^packing/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "mm.models.Packing"}, "edit_packing"),
    url(r'^packing/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "mm.models.Packing"}, "view_packing"),

    url(r'^quantity/$', 'views.generalclass.newlist', {"classname": "mm.models.Quantity"}),
    url(r'^quantity/new/$', 'views.generalclass.newnew', {"classname": "mm.models.Quantity"}, "create_quantity"),
    url(r'^quantity/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "mm.models.Quantity"}, "view_quantity"),
    url(r'^quantity/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "mm.models.Quantity"}, "edit_quantity"),

    url(r'^unit/quantity/(?P<dependent_on_id>\d*)/$', 'views.generalclass.newlist', {"classname": "mm.models.Unit", "dependent_on": ["quantity", "mm.models.Quantity"]}, ),
    url(r'^unit/quantity/(?P<dependent_on_id>\d*)/new/$', 'views.generalclass.newnew', {"classname": "mm.models.Unit", "dependent_on": ["quantity", "mm.models.Quantity"]}, "create_unit"),
    url(r'^unit/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "mm.models.Packing"}, "edit_unit"),
    url(r'^unit/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "mm.models.Packing"}, "view_unit"),

    url(r'^uc/$', 'views.generalclass.newlist', {"classname": "mm.models.Uc"}),
    url(r'^uc/new/$', 'views.generalclass.newnew', {"classname": "mm.models.Uc"}, "create_uc"),
    url(r'^uc/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "mm.models.Uc"}, "view_uc"),
    url(r'^uc/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "mm.models.Uc"}, "edit_uc"),

    url(r'^rgroup/$', 'views.generalclass.newlist', {"classname": "mm.models.RGroup"}),
    url(r'^rgroup/new/$', 'views.generalclass.newnew', {"classname": "mm.models.RGroup"}, "create_rgroup"),
    url(r'^rgroup/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "mm.models.RGroup"}, "view_rgroup"),
    url(r'^rgroup/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "mm.models.RGroup"}, "edit_rgroup"),

    url(r'^rcode/rgroup/(?P<dependent_on_id>\d*)/$', 'views.generalclass.newlist', {"classname": "mm.models.Rcode", "dependent_on": ["rgroup", "mm.models.RGroup"]}, ),
    url(r'^rcode/rgroup/(?P<dependent_on_id>\d*)/new/$', 'views.generalclass.newnew', {"classname": "mm.models.Rcode", "dependent_on": ["rgroup", "mm.models.RGroup"]}, "create_rcode"),
    url(r'^rcode/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "mm.models.Rcode"}, "edit_rcode"),
    url(r'^rcode/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "mm.models.Rcode"}, "view_rcode"),

    url(r'^mtype/$', 'views.generalclass.newlist', {"classname": "mm.models.Mtype"}),
    url(r'^mtype/new/$', 'views.generalclass.newnew', {"classname": "mm.models.Mtype"}, "create_mtype"),
    url(r'^mtype/view/(?P<id>\d*)/$', 'views.generalclass.view', {"classname": "mm.models.Mtype"}, "view_mtype"),
    url(r'^mtype/edit/(?P<id>\d*)/$', 'views.generalclass.edit', {"classname": "mm.models.Mtype"}, "edit_mtype"),


)
