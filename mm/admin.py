from django.contrib import admin
from mm.models import Sup,Pgroup,Packing,Psr,Rgroup,Rcode,Uc,Unit,Quantity

import datetime

class SupAdmin(admin.ModelAdmin):
    model=Sup

from sd.models import Plist
class PlistInline(admin.TabularInline):
    model=Plist
    extra=2

class PackingInline(admin.TabularInline):
    model=Packing
    list_display= ('inv_1','inv_2')
    exclude=('dlfixed','cfactor','series')


class PgroupAdmin(admin.ModelAdmin):
    list_display=['groupname']
    list_filter=['bs_cat']
    ordering=['groupname',]
    search_fields=['groupname',]
    fieldsets=((None,{'fields':('rmarea_id',('groupname','bs_cat'),)})),

    def queryset(self, request):
        return super(PgroupAdmin, self).queryset(request).filter(isactive=True)



class PackingAdmin(admin.ModelAdmin):
    search_fields=['packname',]
    inlines=[PlistInline]

class RgroupAdmin(admin.ModelAdmin):
    model=Rgroup
    list_filter=['dept']
    search_fields=['groupname',]
    ordering=['groupname',]

class RcodeAdmin(admin.ModelAdmin):
    model=Rcode

class UnitAdmin(admin.ModelAdmin):
    model=Unit

class UcInline(admin.TabularInline):
    model=Uc

class QuantityAdmin(admin.ModelAdmin):
    model=Quantity
    inlines=[UcInline]

admin.site.register(Quantity,QuantityAdmin)

admin.site.register(Rgroup,RgroupAdmin)
admin.site.register(Rcode,RcodeAdmin)
admin.site.register(Sup,SupAdmin)

admin.site.register(Pgroup, PgroupAdmin)
admin.site.register(Packing, PackingAdmin)

admin.site.register(Unit,UnitAdmin)
