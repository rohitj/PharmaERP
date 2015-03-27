from django.contrib import admin
from pf2.es.models import Clt,Emp,Fgarea,Station,Pageno,Rep,PageRep,Salecode,Saletax,Rmarea,UserProfile
from pf2.es.models import Bptype,Bpartner

import datetime

class BptypeAdmin(admin.ModelAdmin):
    model=Bptype

class BpartnerAdmin(admin.ModelAdmin):
    model=Bpartner

class CltAdmin(admin.ModelAdmin):
    model=Clt

class EmpAdmin(admin.ModelAdmin):
    model=Emp

class UserProfileAdmin(admin.ModelAdmin):
    model=UserProfile

class FgareaAdmin(admin.ModelAdmin):
    model=Fgarea

class StationAdmin(admin.ModelAdmin):
    model=Station

class PagenoAdmin(admin.ModelAdmin):
    model=Pageno

class PageRepAdmin(admin.ModelAdmin):
    model=PageRep

class RepAdmin(admin.ModelAdmin):
    model=Rep

class SalecodeAdmin(admin.ModelAdmin):
    model = Salecode

class SaletaxAdmin(admin.ModelAdmin):
    model = Saletax

class RmareaAdmin(admin.ModelAdmin):
    model=Rmarea

admin.site.register(Bptype,BptypeAdmin)
admin.site.register(Bpartner,BpartnerAdmin)
admin.site.register(Rmarea,RmareaAdmin)
admin.site.register(Saletax,SaletaxAdmin)
admin.site.register(Salecode,SalecodeAdmin)
admin.site.register(PageRep,PageRepAdmin)
admin.site.register(Station,StationAdmin)
admin.site.register(Pageno,PagenoAdmin)
admin.site.register(Emp,EmpAdmin)
admin.site.register(Rep,RepAdmin)
admin.site.register(Clt,CltAdmin)
admin.site.register(Fgarea,FgareaAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
