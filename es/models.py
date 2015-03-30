from django.db import models
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
import os
from django.core.urlresolvers import resolve

#----------------------------------------------------------------------------------------------------------------------
#  ES Module:  Enterprise Structure model with Client | Business partners | Parties place orders | Sale Areas | Sale Tax | Employee
#-------------------------------------------------------------------------------------------------------------------------


class MyModel(models.Model):
    _classname=""

    @models.permalink
    def create_url(self, request, extra_params=None):
        return ("create_" + self._classname.lower(), (), extra_params)
        
    @models.permalink
    def edit_url(self, request=None):
        return ("edit_"+self._classname.lower(), (), {'id':self.id})

    @models.permalink
    def view_url(self, request=None):
        return ("view_"+self._classname.lower(), (), {'id':self.id})

    @models.permalink
    def delete_url(self, request=None):
        return ("delete_"+self._classname.lower(), (), {'id':self.id})

    def display_name(self, request):
        return self._classname

    def view_template(self, request):
        template = os.path.join(self._meta.app_label, "view"+self._classname.lower()+".html") 
        temp = os.path.join(settings.BASE_DIR, self._meta.app_label, "templates", template)
        if os.path.isfile(os.path.join(settings.BASE_DIR, temp)):
          return template
        return "view.html"
        
    def link_template(self, request):
        template = os.path.join(self._meta.app_label, "link"+self._classname.lower()+".html") 
        temp = os.path.join(settings.BASE_DIR, self._meta.app_label, "templates", template)
        if os.path.isfile(os.path.join(settings.BASE_DIR, temp)):
          return template
        return "link.html"

    def list_template(self, request):
        return "list.html"

    def new_template(self, request):
        template = os.path.join(self._meta.app_label, "new"+self._classname.lower()+".html") 
        temp = os.path.join(settings.BASE_DIR, self._meta.app_label, "templates", template)
        if os.path.isfile(os.path.join(settings.BASE_DIR, temp)):
          return template
        return "new.html"

    def edit_template(self, request):
        template = os.path.join(self._meta.app_label, "edit"+self._classname.lower()+".html") 
        temp = os.path.join(settings.BASE_DIR, self._meta.app_label, "templates", template)
        if os.path.isfile(os.path.join(settings.BASE_DIR, temp)):
          return template
        return "edit.html"
        
    def is_create_allowed(self, request):
        return True

    def is_edit_allowed(self, request):
        return True

    @models.permalink
    def add_dependent_url(self, request=None):
        return ("add_dependent_" + self._classname.lower(), (), {'id':self.id})

    def dependent(self, request, classname_nested=None):
        return None


    def add_dependent_template(request):
        return "add_dependent_" + self._classname.lower() + ".html"


    def newObjectContent(self, request):
        return ""
        
        
    class Meta:
        abstract=True
        
    def updateForms(self, request, form, formset):
        return form, formset


class Code(MyModel):
    name=models.CharField(max_length=60)
    address=models.CharField(max_length=60,null=True,blank=True)
    SUPERCLASS_CHOICES=(("ASSETS","ASSETS"),("LIABILITIIES","LIABILITIIES"),("EXPENDITURE","EXPENDITURE"))
    superclass= models.CharField(max_length=15,choices=SUPERCLASS_CHOICES,null=True,blank=True)
    GCLASS_CHOICES=(("CUS","CUSTOMER"),("SUP","SUPPLIER"),("REP","REPRESENTATIVE"),("EMP","Employee"),("CON","Contacts"),("PSP","Product Supplier"),("OTH","Others"))
    gclass=models.CharField(max_length=3,choices=GCLASS_CHOICES,null=True,blank=True)
    sclass=models.CharField(max_length=3,choices=GCLASS_CHOICES,null=True,blank=True)
    ssclass=models.CharField(max_length=3,choices=GCLASS_CHOICES,null=True,blank=True)
    schedule=models.CharField(max_length=15,null=True,blank=True)


class Employee(Code):
    _classname="Employee"
    user=models.OneToOneField(User)
    jdate=models.DateField()
    designation=models.CharField(max_length=30,blank=True,null=True)
    mobile=models.CharField(max_length=10,blank=True,null=True)
    isexternal=models.BooleanField(default=False)
 #   bptype_id=models.ForeignKey(Bptype,blank=True,null=True)
    bparea=models.CharField(max_length=2,blank=True,null=True)   # business partner area say UG

    def __str__(self):
        return '%s ' % (self.name)

    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(self.name, self.user.username, self.mobile, self.designation)

    def as_table_header(self):
        return "<th>Name</th><th>Username</th><th>Mobile</th><th>designation</th>"

        


class EmployeeForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Employee
        exclude=("user",)


# Business partner types
class BPtype(MyModel):
    _classname="BPtype"
    name=models.CharField(max_length=40)

    def __str__(self):
        return '%s ' % (self.name)

    def as_table(self):
        return "<td>%s</td>"%(self.name)

    def as_table_header(self):
        return "<th>Name</th>"

class BPtypeForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(BPtypeForm, self).__init__(*args, **kwargs)

    class Meta:
        model=BPtype
        exclude=()

# List of business partners 
class BPartner(Code):
    _classname="BPartner"
    bptype=models.ManyToManyField(BPtype)

    def __str__(self):
        return '%s ' % (self.name)

    def as_table(self):
        return "<td>%s</td><td>%s</td>"%(self.name, self.bptype.all())

    def as_table_header(self):
        return "<th>Name</th><th>Type</th>"

    def display_name(self, request):
        return "Business Partner"


class BPartnerForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(BPartnerForm, self).__init__(*args, **kwargs)

    class Meta:
        model=BPartner
        exclude=()




# Top level structure unit for enterprise
class ClientDetails(MyModel):
    _classname="ClientDetails"
    name = models.CharField(max_length=100)
    ce_no=models.CharField(max_length=30)
    dl_head=models.CharField(max_length=40)
    def_area=models.CharField(max_length=2)

    def __str__(self):
        return self.name

    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(self.name, self.ce_no, self.dl_head, self.def_area)

    def as_table_header(self):
        return "<th>Name</th><th>Ce No</th><th>DL Head</th><th>DEF Area</th>"

    def display_name(self, request):
        return "Client Details"


class ClientDetailsForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(ClientDetailsForm, self).__init__(*args, **kwargs)

    class Meta:
        model=ClientDetails
        exclude=()


# Location/Pants assigned to CLT
class Plant(MyModel):
    _classname="Plant"
#    clt_id=models.ForeignKey(Clt)
    name=models.CharField(max_length=30)
    code=models.CharField(max_length=2)
    TYPES=(('PF',u'Internal'),('MB',u'Manufactured By'),('LL',u'Loan Licensing'))
    mode=models.CharField(max_length=2,choices=TYPES)
    clt=models.CharField(max_length=2)

    def __str__(self):
        return "%s"% (self.name)

#    def lastorder(self):
#        from pf2.pp.models import Pordermaster
#        return "Text"  #Pordermaster.objects.all().aggregate(Max("date"))

    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(self.name, self.code, self.mode, self.clt)

    def as_table_header(self):
        return "<th>Name</th><th>Code</th><th>Mode</th><th>clt</th>"


class PlantForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(PlantForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Plant
        exclude=()


# Sales areas (Depo / warehouse etc)
class Depo(MyModel):
    _classname="Depo"
    TYPES=(('PR',u'Production'),('CF',u'Carry & Forarding'),('CI',u'Consingnee Agent'))
    name=models.CharField(max_length=30)
    type=models.CharField(max_length=2,choices=TYPES)
    bottom_1=models.CharField(max_length=80,null=True,blank=True)
    bottom_2=models.CharField(max_length=80,null=True,blank=True)

    def __str__(self):
        return self.name
    def as_table(self):
        return "<td>%s</td><td>%s</td>"%(self.name, self.type)

    def as_table_header(self):
        return "<th>Name</th><th>type</th>"


class DepoForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(DepoForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Depo
        exclude=()



# Marketing location centre 
class Station(MyModel):
    _classname="Station"
#    fgarea_id=models.ForeignKey(Fgarea)
    name=models.CharField(max_length=20)
    asm=models.ForeignKey(Employee)

    def __str__(self):
        return self.name

    def as_table(self):
        return "<td>%s</td><td>%s</td>"%(self.name, self.asm)

    def as_table_header(self):
        return "<th>Name</th><th>ASM</th>"


class StationForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(StationForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Station
        exclude=()


# Subunit of Sales Area represented by one marketing representative
class Pageno(MyModel):
    _classname="Pageno"
    station=models.ForeignKey(Station)
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def as_table(self):
        return "<td>%s</td><td>%s</td>"%(self.name, self.station)

    def as_table_header(self):
        return "<th>Name</th><th>Station</th>"


class PagenoForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(PagenoForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Pageno
        exclude=("station",)


# marketing representative master
class Representative(MyModel):
    _classname="Representative"
    employee=models.OneToOneField(Employee)
    currentpage=models.ForeignKey(Pageno)
#    fgarea_id=models.ForeignKey(Fgarea)

    def __str__(self):
        return '%s %s' % (self.code,self.currentpage)

    def as_table(self):
        return "<td>%s</td><td>%s</td>"%(self.employee.name, self.currentpage)

    def as_table_header(self):
        return "<th>Name</th><th>Current Page</th>"



class RepresentativeForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(RepresentativeForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Representative
        exclude=()


# Assigning rep to pagenumber at a given date
class PageRep(MyModel):
    _class="PageRep"
    pageno=models.ForeignKey(Pageno)
    representative=models.ForeignKey(Representative)
    start_date=models.DateField('start from')
    end_date=models.DateField('end date')

    def __str__(self):
        return '%s %s ' % (self.rep_id , self.fdate)

    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(self.pageno, self.representative, self.start_date, self.end_date)

    def as_table_header(self):
        return "<th>Page</th><th>Representative</th><th>Start Date</th><th>End Date</th>"

    def display_name(self, request):
        return "Page Representative"


class PageRepForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(PageRepForm, self).__init__(*args, **kwargs)

    class Meta:
        model=PageRep
        exclude=()


#Tax classification based on Sales Area/ Purchase type/ SAles type/ and form type
class SalesTax(Code):
    _classname="SalesTax"
    depo=models.ForeignKey(Depo)
    PURTYPE_CHOICES=(('LP','Local Purchase'),('CP','Central Purchase'))
    purtype=models.CharField(max_length=2,default='LP',choices=PURTYPE_CHOICES)
    SALETYPE_CHOICES=(('LST','Local Sale'),('CST','Central Sale'))
    saletype=models.CharField(max_length=5,default='LP',choices=SALETYPE_CHOICES)
    A_FORM_CHOICES=(('C','C Form'),('ST-35','ST-35'),('F','F') )
    a_form=models.CharField(max_length=10,default='C',choices=A_FORM_CHOICES)
#    salecode=models.ForeignKey('fi.Code')
    taxrate=models.DecimalField(max_digits=10, decimal_places=2)
    narration=models.CharField(max_length=100)
    fdate=models.DateField('effective from')
    tdate=models.DateField()

    def __str__(self):
        return '%s %s ' % (self.saletype , self.a_form)

    class Meta:
        unique_together = (('depo','purtype','saletype','a_form', ),)


    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(self.depo, self.purtype, self.saletype, self.a_form)

    def as_table_header(self):
        return "<th>Depo</th><th>Purchase Type</th><th>Sale Type</th><th>A Form</th>"

    def display_name(self, request):
        return "Sales Tax"



class SalesTaxForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(SalesTaxForm, self).__init__(*args, **kwargs)

    class Meta:
        model=SalesTax
        exclude=()


