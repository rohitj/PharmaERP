from django.contrib import admin
from sd.models import Psr,Plist,Customer,VoucherNo
import datetime


class PlistInline(admin.TabularInline):
    model=Plist
    extra=2

class CustomerAdmin(admin.ModelAdmin):
    model = Customer

    def make_active(modeladmin,request,queryset):
        queryset.update(active=1)
        make_active.short_description="Make customer active"
    actions=[make_active]

class PsrInline(admin.TabularInline):
    list_display=['Packing_id','quantity']
    search_fields=('Packing_id',)
    model=Psr
    extra=10

class VoucherNoAdmin(admin.ModelAdmin):
    fieldsets=((None,{'fields':(('date','cust_id'),)})),
    inlines=[PsrInline]


admin.site.register(VoucherNo, VoucherNoAdmin)
admin.site.register(Customer, CustomerAdmin)
