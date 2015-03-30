from django.contrib import admin
from es.models import *

import datetime

class BPtypeAdmin(admin.ModelAdmin):
    model=BPtype

class BPartnerAdmin(admin.ModelAdmin):
    model=BPartner

class ClientDetailsAdmin(admin.ModelAdmin):
    model=ClientDetails

class EmployeeAdmin(admin.ModelAdmin):
    model=Employee

class DepoAdmin(admin.ModelAdmin):
    model=Depo

class StationAdmin(admin.ModelAdmin):
    model=Station

class PagenoAdmin(admin.ModelAdmin):
    model=Pageno

class PageRepAdmin(admin.ModelAdmin):
    model=PageRep

class RepresentativeAdmin(admin.ModelAdmin):
    model=Representative

class SalesTaxAdmin(admin.ModelAdmin):
    model = SalesTax


class PlantAdmin(admin.ModelAdmin):
    model=Plant

admin.site.register(BPtype,BPtypeAdmin)
admin.site.register(BPartner,BPartnerAdmin)
admin.site.register(Plant,PlantAdmin)
admin.site.register(SalesTax,SalesTaxAdmin)
admin.site.register(PageRep,PageRepAdmin)
admin.site.register(Station,StationAdmin)
admin.site.register(Pageno,PagenoAdmin)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Representative,RepresentativeAdmin)
admin.site.register(ClientDetails,ClientDetailsAdmin)
admin.site.register(Depo,DepoAdmin)
