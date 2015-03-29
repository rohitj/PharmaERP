from django.contrib import admin
from sd.models import Plist,Cust,Vno
from mm.models import Psr
import datetime


class PlistInline(admin.TabularInline):
    model=Plist
    extra=2

class CustAdmin(admin.ModelAdmin):
    model = Cust

    def make_active(modeladmin,request,queryset):
        queryset.update(active=1)
        make_active.short_description="Make customer active"
    actions=[make_active]






#admin.site.register(Vno, VnoAdmin)
admin.site.register(Cust, CustAdmin)
