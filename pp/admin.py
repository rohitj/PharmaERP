from django.contrib import admin
from pf2.pp.models import *
from pf2.es.models import *
from pf2.mm.models import *
from pf2.pp.forms import PoForm
import datetime
from django.forms.models import BaseInlineFormSet


class RmrecipeInline(admin.TabularInline):
    model=Rmrecipe

class RmrecipemasterAdmin(admin.ModelAdmin):
    model=Rmrecipemaster
    inlines=[RmrecipeInline]


class RcodeasAdmin(admin.ModelAdmin):
    model=Rcodeas

class MbatchPoInline(admin.TabularInline):
    model=MbatchPo

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(MbatchPoInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if request.GET.get('area', ''):
            area= request.GET.get('area', '')
        if db_field.name == 'porder_id':
            field.queryset = field.queryset.filter(pordermaster_id__rmarea_id= 1)   #hard coded 1
        return field


class MbatchAdmin(admin.ModelAdmin):
    model=Mbatch
#    search_fields = ['title','content']
    inlines=[MbatchPoInline]
    actions=['newfs']

    def get_form(self,request,obj=None,**kwargs):
        request._obj_ = obj
        self.request=request
        f=super(MbatchAdmin,self).get_form(request,obj)
        return f

    def formfield_for_dbfield(self,dbfield,**kwargs):
        if self.request.GET.get('area', ''):
            area= self.request.GET.get('area', '')
        if dbfield.name=="pgroup_id" and self.request._obj_==None:
            kwargs['queryset']= Pgroup.objects.filter(rmarea_id=1)  #hard coded 1
        return super(MbatchAdmin,self).formfield_for_dbfield(dbfield,**kwargs)

class ContactsAdmin(admin.ModelAdmin):
    model=Contacts

class PtransportAdmin(admin.ModelAdmin):
    model=Ptransport
#    form=PtransportBase

class PorderBase(BaseInlineFormSet):
      pass
class PorderInline(admin.TabularInline):
    model=Porder
#    formset=PorderBase
    extra=2

    def get_formset(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
#            l = list('actual','tdd')
            self.exclude.append("actual")
            self.exclude.append("tdd")
        return super(PorderInline, self).get_formset(request, obj, **kwargs)


    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(PorderInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if request.GET.get('area', ''):
            area= request.GET.get('area', '')
        elif request.GET.get('area', '') and UserProfile.objects.get(userid=request.user.id).isexternal:
            area=UserProfile.objects.get(userid=request.user.id).bparea
        else:
            area=1
        if db_field.name == 'packing_id':
            field.queryset = field.queryset.filter(pgroup_id__rmarea_id= area)
        return field

class PordermasterAdmin(admin.ModelAdmin):
    model=Pordermaster
    fieldsets = ( (None, {'fields': (('rmarea_id','orno','transport_id','who','mmode'), 'date',)        }),    )
#    fields = ( 'orno', 'transport_id','who','mmode', 'date')
#    form=PoForm
#    model=Pordermaster
    inlines=[PorderInline]

    def get_form(self,request,obj=None,**kwargs):
        request._obj_ = obj
        self.request=request
        f=super(PordermasterAdmin,self).get_form(request,obj)
        return f

    def formfield_for_dbfield(self,dbfield,**kwargs):
        if self.request.GET.get('area', ''):
            area= self.request.GET.get('area', '')
        elif self.request.GET.get('area', '') and UserProfile.objects.get(userid=self.request.user.id).isexternal:
            area=UserProfile.objects.get(userid=self.request.user.id).bparea
        else:
            area=1
        if dbfield.name=="transport_id" and self.request._obj_==None:
            kwargs['queryset']= Ptransport.objects.filter(rmarea_id=area)
        if dbfield.name=="who" and self.request._obj_==None:
            kwargs['queryset']= Contacts.objects.filter(rmarea_id=area)
        if dbfield.name=="rmarea_id" and self.request._obj_==None:
            kwargs['queryset']= Rmarea.objects.filter(id=area)

        return super(PordermasterAdmin,self).formfield_for_dbfield(dbfield,**kwargs)

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if not hasattr(instance,'created_by'):
            instance.userid = request.user
            instance.save()
        form.save_m2m()
        return instance

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
           instance.tdd=instance.edd
        instance.save()
        formset.save_m2m()

admin.site.register(Mbatch,MbatchAdmin)
admin.site.register(Rmrecipemaster,RmrecipemasterAdmin)
admin.site.register(Ptransport,PtransportAdmin)
admin.site.register(Pordermaster,PordermasterAdmin)
admin.site.register(Contacts,ContactsAdmin)
admin.site.register(Rcodeas,RcodeasAdmin)