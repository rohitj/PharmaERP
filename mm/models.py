from django.db import models
from django.forms import ModelForm
from django import forms
import datetime
from django.core.urlresolvers import resolve

#------------------------------------------------------------------------------------------------


#from es.models import Rmarea
#from pp.models import Rmrecipe
class Pgroup(models.Model):
    groupname = models.CharField(max_length=60)
    bs_cat=models.CharField(max_length=10,null=True,blank=True)
    rmarea_id=models.ForeignKey('es.Rmarea')
    isactive=models.BooleanField(default=True)

    def required(self,b,dep):
         from pp.models import Rmrecipemaster,Rmrecipe
         qty=b.batchsize()

         if dep=="RM":
             q=Rmrecipemaster.objects.filter(pgroup_id=self, fdate__lt= datetime.date.today(), tdate__gt=datetime.date.today())
             f= q[0].rmrecipe_set.all().extra(select={"treq":0,"alloted":0})
             for item in f:
                item.treq=item.cal(qty)
                item.nreq=0.00
         else:
             q=Pmrecipemaster.objects.filter(pgroup_id=self, fdate__lt= datetime.date.today(), tdate__gt=datetime.date.today())
             f= q[0].pmrecipe_set.all()

         return f

    def __str__(self):
        return "%s" % (self.groupname)


    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(self.groupname, self.bs_cat, self.rmarea_id, self.isactive)

    def as_table_header(self):
        return "<th>Name</th><th>BS Cat</th><th>RMArea</th><th>isActive</th>"

    @models.permalink
    def create_url(request):
        return ("create_pgroup", (), {})
        
    @models.permalink
    def edit_url(self, request=None):
        return ("edit_pgroup", (), {'id':self.id})

    @models.permalink
    def view_url(self, request=None):
        return ("view_pgroup", (), {'id':self.id})

    def display_name(self, request):
        return "Product Group"

    def template(request):
        return "general_result.html"

    def view_template(self, request):
        return "mm/viewpgroup.html"
        
    def link_template(request):
        return "mm/linkpgroup.html"

    def edit_template(request):
        return "mm/editpgroup.html"
        
    def is_create_allowed(request):
        return True

    def is_edit_allowed(self, request):
        return True

    def dependent(self, request, classname_nested=None):
        return self.packing_set.all()


class PgroupForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(PgroupForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Pgroup

class Packing(models.Model):
    pgroup_id=models.ForeignKey(Pgroup)
    packname=models.CharField(max_length=30)
#    packgroup=models.CharField(max_length=4)  #same packing with small vriation. analysis can be done with this group
    tab_tp=models.CharField(max_length=1,null=True)
    unitppack=models.IntegerField(null=True,blank=True)
    qty_per_ca=models.IntegerField(null=True,blank=True)
    box=models.IntegerField(null=True,blank=True)
    ptype=models.IntegerField(null=True,blank=True)
    cfactor=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    rate_cs=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    rate_bsd=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    rate_bsg=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    inv_1=models.IntegerField(null=True,blank=True)
    inv_2=models.IntegerField(null=True,blank=True)
    btype=models.IntegerField(null=True,blank=True)
    dlfixed=models.CharField(max_length=10,null=True,blank=True)
    series=models.IntegerField(null=True,blank=True)
    SS= (('1',u'Sale'),('2','Sample'))
    sale_or_sample=models.CharField(max_length=1,default='D',choices=SS)

    def __str__(self):
        return '%s %s'        % (self.pgroup_id,self.packname)

    def fst(self):
        return 10

    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(self.packname, self.unitppack, self.qty_per_ca, self.box)

    def as_table_header(self):
        return "<th>Name</th><th>Unit Pack</th><th>QTY Per CA</th><th>Box</th>"

    @models.permalink
    def add_dependent_url(self, request=None):
        return ("add_dependent_pgroup", (), {'id':self.id})

    @models.permalink
    def create_url(request):
        return ("create_pgroup", (), {})
        
    @models.permalink
    def edit_url(self, request=None):
        return ("edit_pgroup", (), {'id':self.id})

    @models.permalink
    def view_url(self, request=None):
        return ("view_packing", (), {'id':self.id})

    def display_name(self, request):
        return "Packings"

    def template(request):
        return "general_result.html"

    def view_template(self, request):
        return "mm/viewpacking.html"
        
    def link_template(request):
        return "mm/linkpacking.html"

    def edit_template(self, request):
        return "mm/editpacking.html"
        
    def is_create_allowed(request):
        return True

    def is_edit_allowed(self, request):
        return True


class PackingForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(PackingForm, self).__init__(*args, **kwargs)

    def save(self, request, commit=True):
        instance = super(PackingForm, self).save(commit=False)
        func, args, kwargs = resolve(request.path)
        instance.pgroup_id = Pgroup.objects.get(pk=kwargs["dependent_id"])
        if commit:
            instance.save()
        return instance
#        blah.pgroup_id = re

    class Meta:
        model=Packing
        exclude=("pgroup_id",)



class Psup(models.Model):         #product suppllier
    code=models.OneToOneField('fi.Code',primary_key=True)

class Recno(models.Model):
    psup_id=models.ForeignKey(Psup)
    date=models.DateField('receipt date')

class Pbatch(models.Model):
    recno_id=models.ForeignKey(Recno)
    batchname=models.CharField(max_length=20)
    expiery=models.DateField('expiery date')

#from sd.models import Vno
class Psr(models.Model):
    vno_id=models.ForeignKey("sd.Vno",blank=True,null=True)
    pack_id=models.ForeignKey(Packing)
    pbatch_id=models.ForeignKey(Pbatch)
    fullcases=models.IntegerField(null=True,blank=True)
    looseqty=models.IntegerField(null=True,blank=True)
    quantity=models.DecimalField(max_digits=10, decimal_places=0)
#    price

    def __str__(self):
        return ' '
#------------------------------------------------------------------------------------------------
class Unit(models.Model):
    name=models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.name


class Quantity(models.Model):
    name=models.CharField(max_length=10)
    unit=models.ForeignKey(Unit)

    def __str__(self):
        return self.name


class Uc(models.Model):
    quantity_id=models.ForeignKey(Quantity)
    u1=models.ForeignKey(Unit,related_name='fromunit')
    u2=models.ForeignKey(Unit,related_name='tounit')
    factor=models.DecimalField(max_digits=10,decimal_places=4)

    def __str__(self):
        return "%s %s " % (self.u1 + "-->"+  self.u2)


class Rgroup(models.Model):
    groupname = models.CharField(max_length=60)
    DEPT_CHOICES=(('RM','Raw Material'),('PM','Packing Material'))
    dept=models.CharField(max_length=2,choices=DEPT_CHOICES)
    family=models.CharField(max_length=6,blank=True,null=True)

    def __str__(self):
        return self.groupname

    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td>"%(self.groupname, self.dept, self.family)

    def as_table_header(self):
        return "<th>Name</th><th>Dept</th><th>Family</th>"

    @models.permalink
    def create_url(request):
        return ("create_rgroup", (), {})
        
    @models.permalink
    def edit_url(self, request=None):
        return ("edit_rgroup", (), {'id':self.id})

    @models.permalink
    def view_url(self, request=None):
        return ("view_rgroup", (), {'id':self.id})

    def display_name(self, request):
        return "Raw Material Group"

    def template(request):
        return "general_result.html"

    def view_template(self, request):
        return "mm/viewrgroup.html"
        
    def link_template(request):
        return "mm/linkrgroup.html"

    def edit_template(request):
        return "mm/editrgroup.html"
        
    def is_create_allowed(request):
        return True

    def is_edit_allowed(self, request):
        return True

    def dependent(self, request, classname_nested=None):
        return self.rcode_set.all()

class RgroupForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(RgroupForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Rgroup

#from es.models import Rmarea
class Rcode(models.Model):
    rgroup_id=models.ForeignKey(Rgroup)
    rname=models.CharField(max_length=60)
    UNIT_CHOICES=(('GM','Grams'),('KG','Kilograms'),('LT','Litres'),('NO','Numbers'))
    unit=models.CharField(max_length=2,choices=UNIT_CHOICES)
    rmarea_id=models.ForeignKey('es.Rmarea',blank=True,null=True)  #some material belong to an area
    rcd=models.CharField(max_length=6,blank=True,null=True)

    def __str__(self):
        return self.rname

    def av(self):
        rid=self.id
        return self.rbatch_set.raw("select a.id,a.rcode_id_id,a.quantity,sum(b.quantity) as used,(a.quantity-sum(b.quantity)) as bal from mm_rbatch a,mm_rsr b where a.rcode_id_id=%s and a.id=b.rbatch_id_id group by a.id having a.quantity>used",[rid])

    def as_table(self):
        return "<td>%s</td>"%(self.name)

    def as_table_header(self):
        return "<th>Name</th>"

    @models.permalink
    def create_url(request):
        return ("create_rcode", (), {})
        
    @models.permalink
    def edit_url(self, request=None):
        return ("edit_rcode", (), {'id':self.id})

    @models.permalink
    def view_url(self, request=None):
        return ("view_rcode", (), {'id':self.id})

    def display_name(self, request):
        if self.rgroup_id:
            return "Packing for " + self.rgroup_id
        return "Packing"

    def template(request):
        return "general_result.html"

    def view_template(self, request):
        return "mm/viewrcode.html"
        
    def link_template(request):
        return "mm/linkrcode.html"

    def edit_template(request):
        return "mm/editrgroup.html"
        
    def is_create_allowed(request):
        return True

    def is_edit_allowed(self, request):
        return True

class RcodeForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(RcodeForm, self).__init__(*args, **kwargs)

    def save(self, request, commit=True):
        instance = super(RcodeForm, self).save(commit=False)
        func, args, kwargs = resolve(request.path)
        instance.rgroup_id = Rgroup.objects.get(pk=kwargs["dependent_id"])
        if commit:
            instance.save()
        return instance

    class Meta:
        model=Rcode
        exclude=("rgroup_id",)


class Mtype(models.Model):
#    USAGE_CHOICES=(("O","Opening Balance"),("P","Purchase"),("M","Miscellaneous"),("R","Reserved"))
    mtype=models.PositiveIntegerField(primary_key=True)
    description=models.CharField(max_length=20,null=True)

class Pur(models.Model):
    sup_id=models.ForeignKey(Sup)
    REF_CHOICES=(("JV","Challan"),("PI","Purchase Bill"))
    ref=models.CharField(max_length=2,choices=REF_CHOICES)
    date=models.DateField(null=True)
    billno=models.CharField(max_length=20,blank=True,null=True)
    billdate=models.DateField(null=True,blank=True)
    aform=models.CharField(max_length=10,blank=True,null=True)
    aformno=models.CharField(max_length=20,null=True,blank=True)
    amount=models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)
    saletax=models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)
    excise=models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)
    exciseinv=models.IntegerField(null=True,blank=True)
    others=models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)
    ismodvat=models.BooleanField()
    thno=models.CharField(max_length=10,null=True)
    typesup=models.CharField(max_length=10,null=True)
    typedoc=models.CharField(max_length=10,null=True)
    discount=models.DecimalField(max_digits=12, decimal_places=2)
    freight=models.DecimalField(max_digits=12, decimal_places=2)
    challanno=models.DecimalField(max_digits=12, decimal_places=2)
    paydays=models.IntegerField()
    misc=models.IntegerField()
    modvatcat=models.IntegerField()

    ino=models.IntegerField(unique_for_year="date")  #internal purchase no.

class Rbatch(models.Model):
    pur_id=models.IntegerField(null=True,blank=True)
    rcode_id=models.ForeignKey(Rcode)
    batchno=models.CharField(max_length=20,blank=True,null=True)
    trno=models.CharField(max_length=20,blank=True,null=True)
    mtype_id=models.ForeignKey(Mtype)   #assgn one for reservation
    quantity=models.DecimalField(max_digits=12, decimal_places=2)
    rate=models.DecimalField(max_digits=12, blank=True,null=True,decimal_places=2)
    rate_cost=models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)
    modvatcat=models.IntegerField(blank=True,null=True)
    excise=models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)
    cess=models.DecimalField(max_digits=12, decimal_places=2,blank=True,null=True)
    aform=models.CharField(max_length=10,null=True,blank=True)
    thno=models.CharField(max_length=10,null=True,blank=True)
    typesup=models.CharField(max_length=10,null=True,blank=True)
    typedoc=models.CharField(max_length=10,null=True,blank=True)
    ismodvat=models.BooleanField()
    purity=models.DecimalField(max_digits=12, decimal_places=2,default=1)
    ispass=models.BooleanField()  #Pass or fail
    mfrr=models.CharField(max_length=40,blank=True,null=True)
    mfgdate=models.DateField(null=True,blank=True)
    lst=models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)
    cst=models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)
    expiery=models.DateField(null=True,blank=True)

    def _bal(self):
        return 10

    balance = property(_bal)

#quality data shall flow from existing system

#from pp.models import Fstype
#from es.models import Rmarea
class Rsr(models.Model):
    fstype_id=models.ForeignKey('pp.Fstype',null=True,blank=True)
    tab_tp=models.CharField(max_length=1,blank=True,null=True)
    date=models.DateField(default=datetime.date.today())
    rbatch_id=models.ForeignKey(Rbatch)
    mtype_id=models.ForeignKey(Mtype)   #movement type
    quantity=models.DecimalField(max_digits=12, decimal_places=4)
    areato=models.ForeignKey('es.Rmarea', blank=True,null=True)


class Test(models.Model):
      packing_id=models.ForeignKey(Packing,blank=True,null=True)
      test=models.CharField(max_length=100)



