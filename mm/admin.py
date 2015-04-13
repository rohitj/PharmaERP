from django.contrib import admin
from mm.models import PGroup,Packing,RGroup,Rcode,Uc,Unit,Quantity,Supplier
import datetime


#from sd.models import Plist
#class PlistInline(admin.TabularInline):
#    model=Plist
#    extra=2

class SupplierAdmin(admin.ModelAdmin):
    model=Supplier


class PackingInline(admin.TabularInline):
    model=Packing
    list_display= ('inv_1','inv_2')
    exclude=('dlfixed','cfactor','series')


class PGroupAdmin(admin.ModelAdmin):
    list_display=['name']
    list_filter=['bs_cat']
    ordering=['name',]
    search_fields=['name',]
    fieldsets=((None,{'fields':('plant',('name','bs_cat'),)})),

    def get_queryset(self, request):
        return super(PGroupAdmin, self).queryset(request).filter(isactive=True)



#class PackingAdmin(admin.ModelAdmin):
#    search_fields=['packname',]
#    inlines=[PlistInline]

class RGroupAdmin(admin.ModelAdmin):
    model=RGroup
    list_filter=['dept']
    search_fields=['name',]
    ordering=['name',]

class RcodeAdmin(admin.ModelAdmin):
    model=Rcode

class UnitAdmin(admin.ModelAdmin):
    model=Unit

class QuantityAdmin(admin.ModelAdmin):
    model=Quantity

admin.site.register(Quantity,QuantityAdmin)

admin.site.register(RGroup,RGroupAdmin)
admin.site.register(Rcode,RcodeAdmin)

admin.site.register(PGroup, PGroupAdmin)
#admin.site.register(Packing, PackingAdmin)

admin.site.register(Unit,UnitAdmin)
admin.site.register(Supplier,SupplierAdmin)
