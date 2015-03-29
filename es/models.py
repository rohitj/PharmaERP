from django.db import models
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

class Code(models.Model):
    name=models.CharField(max_length=60)
    address=models.CharField(max_length=60,null=True,blank=True)
    SUPERCLASS_CHOICES=(("ASSETS","ASSETS"),("LIABILITIIES","LIABILITIIES"),("EXPENDITURE","EXPENDITURE"))
    superclass= models.CharField(max_length=15,choices=SUPERCLASS_CHOICES,null=True,blank=True)
    GCLASS_CHOICES=(("CUS","CUSTOMER"),("SUP","SUPPLIER"),("REP","REPRESENTATIVE"),("EMP","Employee"),("CON","Contacts"),("PSP","Product Supplier"),("OTH","Others"))
    gclass=models.CharField(max_length=3,choices=GCLASS_CHOICES,null=True,blank=True)
    sclass=models.CharField(max_length=3,choices=GCLASS_CHOICES,null=True,blank=True)
    ssclass=models.CharField(max_length=3,choices=GCLASS_CHOICES,null=True,blank=True)
    schedule=models.CharField(max_length=15,null=True,blank=True)

    def __str__(self):
        return "%s %s %s %s" % (self.name, self.superclass, self.gclass,self.test())

    def test(self):
         return "OK"
    class Meta:
         verbose_name = "Account Head"


class Employee(Code):
    user=models.OneToOneField(User)
    jdate=models.DateField()
    designation=models.CharField(max_length=30,blank=True,null=True)
    mobile=models.CharField(max_length=10,blank=True,null=True)
    isexternal=models.BooleanField(default=False)
 #   bptype_id=models.ForeignKey(Bptype,blank=True,null=True)
    bparea=models.CharField(max_length=2,blank=True,null=True)   # business partner area say UG

    def __str__(self):
        return '%s ' % (self.code)

    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(self.name, self.code, self.mode, self.clt)

    def as_table_header(self):
        return "<th>Name</th><th>Code</th><th>Mode</th><th>clt</th>"

    @models.permalink
    def create_url(request):
        return ("create_employee", (), {})
        
    @models.permalink
    def edit_url(self, request=None):
        return ("edit_employee", (), {'id':self.id})

    @models.permalink
    def view_url(self, request=None):
        return ("view_employee", (), {'id':self.id})

    def display_name(self, request):
        return "Employee"

    def template(request):
        return "general_result.html"

    def view_template(request):
        return "es/viewemployee.html"
        
    def link_template(request):
        return "es/linkemployee.html"

    def edit_template(request):
        return "es/editemployee.html"
        
    def is_create_allowed(request):
        return True

    def is_edit_allowed(request):
        return True


class EmployeeForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Employee
        exclude=()


class BPtype(models.Model):
    name=models.CharField(max_length=40)

    def __str__(self):
        return '%s ' % (self.name)


class BPartner(Code):
    name=models.CharField(max_length=60)
    bptype=models.ManyToManyField(BPtype)

    def __str__(self):
        return '%s ' % (self.name)




class ClientDetails(models.Model):
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

    @models.permalink
    def create_url(request):
        return ("create_client", (), {})
        
    @models.permalink
    def edit_url(self, request=None):
        return ("edit_client", (), {'id':self.id})

    @models.permalink
    def view_url(self, request=None):
        return ("view_client", (), {'id':self.id})

    def display_name(self, request):
        return "Client"

    def template(request):
        return "general_result.html"

    def view_template(request):
        return "viewclient.html"
        
    def link_template(request):
        return "es/linkclient.html"

    def edit_template(self, request):
        return "es/editclient.html"
        
    def is_create_allowed(request):
        return True

    def is_edit_allowed(self, request):
        return True


class ClientDetailsForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Client
        exclude=()


class Plant(models.Model):
    clt_id=models.ForeignKey(Clt)
    name=models.CharField(max_length=30)
    code=models.CharField(max_length=2)
    TYPES=(('PF',u'Internal'),('MB',u'Manufactured By'),('LL',u'Loan Licensing'))
    mode=models.CharField(max_length=2,choices=TYPES)
    clt=models.CharField(max_length=2)

    def __str__(self):
        return "%s"% (self.name)

    def lastorder(self):
        from pf2.pp.models import Pordermaster
        return "Text"  #Pordermaster.objects.all().aggregate(Max("date"))

    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(self.name, self.code, self.mode, self.clt)

    def as_table_header(self):
        return "<th>Name</th><th>Code</th><th>Mode</th><th>clt</th>"

    @models.permalink
    def create_url(request):
        return ("create_plant", (), {})
        
    @models.permalink
    def edit_url(self, request=None):
        return ("edit_plant", (), {'id':self.id})

    @models.permalink
    def view_url(self, request=None):
        return ("view_plant", (), {'id':self.id})

    def display_name(self, request):
        return "Plant"

    def template(request):
        return "general_result.html"

    def view_template(request):
        return "es/viewplant.html"
        
    def link_template(request):
        return "es/linkplant.html"

    def edit_template(request):
        return "es/editplant.html"
        
    def is_create_allowed(request):
        return True

    def is_edit_allowed(request):
        return True


class PlantForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(RmareaForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Rmarea
        exclude=()


class Depo(models.Model):
    TYPES=(('PR',u'Production'),('CF',u'Carry & Forarding'),('CI',u'Consingnee Agent'))
    name=models.CharField(max_length=30)
    type=models.CharField(max_length=2,choices=TYPES)
    bottom_1=models.CharField(max_length=80,null=True,blank=True)
    bottom_2=models.CharField(max_length=80,null=True,blank=True)

    def __str__(self):
        return self.name


class Station(models.Model):
#    fgarea_id=models.ForeignKey(Fgarea)
    name=models.CharField(max_length=20)
    asm=models.ForeignKey(Employee)

    def __str__(self):
        return self.name

class Pageno(models.Model):
    fgarea_id=models.ForeignKey(Fgarea)
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Rep(models.Model):
    emp=models.OneToOneField(Employee,primary_key=True)
    currentpage=models.ForeignKey(Pageno)
#    fgarea_id=models.ForeignKey(Fgarea)

    def __str__(self):
        return '%s %s' % (self.code,self.currentpage)


class PageRep(models.Model):
    pageno_id=models.ForeignKey(Pageno)
    rep_id=models.ForeignKey(Rep)
    fdate=models.DateField('effective from')
    tdate=models.DateField()

    def __str__(self):
        return '%s %s ' % (self.rep_id , self.fdate)

#------------------------------------------------------------------------------------------------


class Sup(Code):
    stno=models.CharField(max_length=30,null=True,blank=True,verbose_name="Sale Tax No")
    eccno=models.CharField(max_length=20,null=True,blank=True)
    identity=models.CharField(max_length=10,null=True,blank=True)
    active=models.BooleanField(default=True)

    def __str__(self):
        return '%s' % (self.code)

class Salecode(Code):
    fgarea_id=models.ForeignKey(Fgarea)
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
        unique_together = (('fgarea_id','purtype','saletype','a_form', ),)




