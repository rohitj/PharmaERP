from django.contrib import admin
from fi.models import Code,Pay,Led
import datetime

class CodeAdmin(admin.ModelAdmin):
    model=Code

class LedAdmin(admin.ModelAdmin):
    model=Led


class PayAdmin(admin.ModelAdmin):
    model=Pay


admin.site.register(Pay,PayAdmin)
admin.site.register(Led,LedAdmin)
admin.site.register(Code,CodeAdmin)
