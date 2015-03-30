from django.contrib import admin
from fi.models import Pay,Led
import datetime


class LedAdmin(admin.ModelAdmin):
    model=Led


class PayAdmin(admin.ModelAdmin):
    model=Pay


admin.site.register(Pay,PayAdmin)
admin.site.register(Led,LedAdmin)
