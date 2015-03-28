from django.db import models
from django.forms import ModelForm
from django import forms
#from pp.models import Pordermaster

#----------------------------------------------------------------------------------------------------------------------
#  ES Module:  Enterprise Structure model with Client | Business partners | Parties place orders | Sale Areas | Sale Tax | Employee
#-------------------------------------------------------------------------------------------------------------------------


# Employee model 
class Emp(models.Model):
    code=models.OneToOneField('fi.Code',primary_key=True)
    jdate=models.DateField()

    def __str__(self):
        return '%s ' % (self.code)

# Business partner types
class Bptype(models.Model):
    name=models.CharField(max_length=40)

    def __str__(self):
        return '%s ' % (self.name)

# Customized user profile for authorization
from django.contrib.auth.models import User
class UserProfile(models.Model):
    userid=models.OneToOneField(User)
    designation=models.CharField(max_length=30,blank=True,null=True)
    mobile=models.CharField(max_length=10,blank=True,null=True)
    address=models.CharField(max_length=100,blank=True,null=True)
    isexternal=models.BooleanField(default=False)
    bptype_id=models.ForeignKey(Bptype,blank=True,null=True)
    bparea=models.CharField(max_length=2,blank=True,null=True)   # business partner area say UG
    emp_id=models.ForeignKey(Emp,blank=True,null=True)

    def __str__(self):
        return '%s ' % (self.userid.username)

# List of business partners 
class Bpartner(models.Model):
    name=models.CharField(max_length=60)
    bptype_id=models.ManyToManyField(Bptype)

    def __str__(self):
        return '%s ' % (self.name)

# Top level structure unit for enterprise
class Clt(models.Model):
    clt_name = models.CharField(max_length=100)
    ce_no=models.CharField(max_length=30)
    dl_head=models.CharField(max_length=40)
    def_area=models.CharField(max_length=2)

    def __str__(self):
        return self.clt_name

# Location/Pants assigned to CLT
class Rmarea(models.Model):
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

# Sales areas (Depo / warehouse etc)
class Fgarea(models.Model):
    clt_id=models.ForeignKey(Clt)
    TYPES=(('PR',u'Production'),('CF',u'Carry & Forarding'),('CI',u'Consingnee Agent'))
    name=models.CharField(max_length=30)
    type=models.CharField(max_length=2,choices=TYPES)
    bottom_1=models.CharField(max_length=80,null=True,blank=True)
    bottom_2=models.CharField(max_length=80,null=True,blank=True)

    def __str__(self):
        return self.name

# Marketing location centre 
class Station(models.Model):
    fgarea_id=models.ForeignKey(Fgarea)
    name=models.CharField(max_length=20)
    asm=models.ForeignKey(Emp)

    def __str__(self):
        return self.name

# Subunit of Sales Area represented by one marketing representative
class Pageno(models.Model):
    fgarea_id=models.ForeignKey(Fgarea)
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name

# marketing representative master
class Rep(models.Model):
    code=models.OneToOneField(Emp,primary_key=True)
    currentpage=models.ForeignKey(Pageno)
    fgarea_id=models.ForeignKey(Fgarea)

    def __str__(self):
        return '%s %s' % (self.code,self.currentpage)

# Assigning rep to pagenumber at a given date
class PageRep(models.Model):
    pageno_id=models.ForeignKey(Pageno)
    rep_id=models.ForeignKey(Rep)
    fdate=models.DateField('effective from')
    tdate=models.DateField()

    def __str__(self):
        return '%s %s ' % (self.rep_id , self.fdate)

#Tax classification based on Sales Area/ Purchase type/ SAles type/ and form type
class Saletax(models.Model):
    fgarea_id=models.ForeignKey(Fgarea)
    PURTYPE_CHOICES=(('LP','Local Purchase'),('CP','Central Purchase'))
    purtype=models.CharField(max_length=2,default='LP',choices=PURTYPE_CHOICES)
    SALETYPE_CHOICES=(('LST','Local Sale'),('CST','Central Sale'))
    saletype=models.CharField(max_length=5,default='LP',choices=SALETYPE_CHOICES)
    A_FORM_CHOICES=(('C','C Form'),('ST-35','ST-35'),('F','F') )
    a_form=models.CharField(max_length=10,default='C',choices=A_FORM_CHOICES)
    salecode=models.ForeignKey('fi.Code')
    taxrate=models.DecimalField(max_digits=10, decimal_places=2)
    narration=models.CharField(max_length=100)
    fdate=models.DateField('effective from')
    tdate=models.DateField()

    def __str__(self):
        return '%s %s ' % (self.saletype , self.a_form)

    class Meta:
        unique_together = (('fgarea_id','purtype','saletype','a_form', ),)

#------------------------------------------------------------------------------------------------









