from django.db import models
from django.forms import ModelForm
from django import forms
import datetime
from django.core.urlresolvers import resolve
from es.models import *

#------------------------------------------------------------------------------------------------
#  MM Module:  Product & raw material | Stock register for both | Unit Mgt | Supplier & purchases
#------------------------------------------------------------------------------------------------


class Supplier(Code):
    _classname="Supplier"
    stno=models.CharField(max_length=30,null=True,blank=True,verbose_name="Sale Tax No")
    eccno=models.CharField(max_length=20,null=True,blank=True)
    identity=models.CharField(max_length=10,null=True,blank=True)
    isActive=models.BooleanField(default=True)

    def __str__(self):
        return '%s' % (self.code)

    def as_table(self):
        return "<td>%s</td>"%(self.name)

    def as_table_header(self):
        return "<th>Name</th>"


class SupplierForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Supplier
        exclude=()


# Product group master [ Each item indicate one product line]
class PGroup(MyModel):
    _classname="PGroup"
    name = models.CharField(max_length=60)
    bs_cat=models.CharField(max_length=10,null=True,blank=True)         # Category as defined by Govt of India.
    plant=models.ForeignKey('es.Plant')
    isactive=models.BooleanField(default=True)                          # Only active allowed for production

#    def required(self,b,dep):
#         from pp.models import Rmrecipemaster,Rmrecipe
#         qty=b.batchsize()
#
#         if dep=="RM":
#             q=Rmrecipemaster.objects.filter(pgroup_id=self, fdate__lt= datetime.date.today(), tdate__gt=datetime.date.today())
#             f= q[0].rmrecipe_set.all().extra(select={"treq":0,"alloted":0})
#             for item in f:
#                item.treq=item.cal(qty)
#                item.nreq=0.00
#         else:
#             q=Pmrecipemaster.objects.filter(pgroup_id=self, fdate__lt= datetime.date.today(), tdate__gt=datetime.date.today())
#             f= q[0].pmrecipe_set.all()
#
#         return f

    def __str__(self):
        return "%s" % (self.name)


    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td><td>%s</td>"%(self.name, self.bs_cat, self.plant, self.isactive)

    def as_table_header(self):
        return "<th>Name</th><th>BS Cat</th><th>RMArea</th><th>isActive</th>"


class PGroupForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(PGroupForm, self).__init__(*args, **kwargs)

    class Meta:
        model=PGroup
        exclude=()


# Indicates one product packing within a product line [ will have individual formulation]
class Packing(MyModel):
    _classname="Packing"
    pgroup=models.ForeignKey(PGroup)
    packname=models.CharField(max_length=30)
#    packgroup=models.CharField(max_length=4)  #same packing with small vriation. analysis can be done with this group
    tab_tp=models.CharField(max_length=1,null=True)             # Should be omitted after discussion.
    unitppack=models.IntegerField(null=True,blank=True)         # How many production units contained in a packing say number of tablet in a packing
    qty_per_ca=models.IntegerField(null=True,blank=True)        # How many packings in a case ( which is used for shipment)
    box=models.IntegerField(null=True,blank=True)               # How many packings in a box ( which is used for shipment)
    ptype=models.IntegerField(null=True,blank=True)             # Don't remember 
    cfactor=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)  # Don't remember
    rate_cs=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)  # Closing stock rate used for financial reporting
    rate_bsd=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)  # Balance sheet related rate used for financial reporting
    rate_bsg=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)  # RT12 report related rate used for financial reporting
    inv_1=models.IntegerField(null=True,blank=True)                     #  Crtical invetory level -I
    inv_2=models.IntegerField(null=True,blank=True)                     #  Crtical invetory level -II
    btype=models.IntegerField(null=True,blank=True)                     # Dont remember
    dlfixed=models.CharField(max_length=10,null=True,blank=True)        # Fixed text for each packing
    series=models.IntegerField(null=True,blank=True)                    # Fixed text used for production
    SS= (('1',u'Sale'),('2','Sample'))                                  # Each packing is designatec as sale or sample item.
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



class PackingForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(PackingForm, self).__init__(*args, **kwargs)

#    def save(self, request, commit=True):
#        instance = super(PackingForm, self).save(commit=False)
#        func, args, kwargs = resolve(request.path)
#        instance.pgroup = PGroup.objects.get(pk=kwargs["dependent_on_id"])
#        if commit:
#            instance.save()
#        return instance

    class Meta:
        model=Packing
        exclude=("pgroup",)



# List of supplier of finished product- Pharmasynth sometimes buy finshed product and market those product. Not to be used.
class Psup(Code):         #product suppllier
    _classname="Psup"

    def __str__(self):
        return '%s'        % (self.name)


    def as_table(self):
        return "<td>%s</td>"%(self.name)

    def as_table_header(self):
        return "<th>Name</th>"




class PsupForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(PsupForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Psup
        exclude=()


# Not to be used.
class Recno(MyModel):
    _classname="Recno"
    psup=models.ForeignKey(Psup)
    date=models.DateField('receipt date')

    def __str__(self):
        return '%s'        % (self.name)

    def as_table(self):
        return "<td>%s</td><td>%s</td>"%(self.name, self.date)

    def as_table_header(self):
        return "<th>Name</th><th>Date</th>"



class RecnoForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(RecnoForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Recno
        exclude=()


# Not to be used.
class Pbatch(MyModel):
    _classname="Pbatch"
    recno=models.ForeignKey(Recno)
    batchname=models.CharField(max_length=20)
    expiery=models.DateField('expiery date')

    def __str__(self):
        return '%s %s'        % (self.pgroup_id,self.packname)


    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td>"%(self.recno, self.batchname, self.expiery)

    def as_table_header(self):
        return "<th>Rec No</th><th>Batch Name</th><th>Expiery</th>"



class PbatchForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(PbatchForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Pbatch
        exclude=()



# Dimension master say VOLUME MASS DENSITY etc.
class Quantity(MyModel):
    _classname="Quantity"
    name=models.CharField(max_length=10)

    def __str__(self):
        return self.name

    def as_table(self):
        return "<td>%s</td>"%(self.name)

    def as_table_header(self):
        return "<th>Name</th>"


class QuantityForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(QuantityForm, self).__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model=Quantity
        exclude=()

# Units -  to be extended with additional fields 
class Unit(MyModel):
    _classname="Unit"
    quantity=models.ForeignKey(Quantity)
    name=models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.name

    def as_table(self):
        return "<td>%s</td>"%(self.name)

    def as_table_header(self):
        return "<th>Name</th>"


class UnitForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Unit
        exclude=("quantity",)

# Unit conversion interface from one unit to another
class Uc(MyModel):
    _classname="Uc"
#    quantity_id=models.ForeignKey(Quantity)
    u1=models.ForeignKey(Unit,related_name='fromunit')
    u2=models.ForeignKey(Unit,related_name='tounit')
    factor=models.DecimalField(max_digits=10,decimal_places=4)

    # TODO: Ensure u1 and u2 are of same quantity type
    def __str__(self):
        return "%s %s " % (self.u1 + "-->"+  self.u2)

    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td>"%(self.u1, self.u2, self.factor)

    def as_table_header(self):
        return "<th>Unit1</th><th>Unit2</th><th>Factor</th>"


class UcForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(UcForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Uc
        exclude=()




#  Material group-  class of input materials
class RGroup(MyModel):
    _classname='RGroup'
    name = models.CharField(max_length=60)
    DEPT_CHOICES=(('RM','Raw Material'),('PM','Packing Material'))
    dept=models.CharField(max_length=2,choices=DEPT_CHOICES)
    family=models.CharField(max_length=6,blank=True,null=True)

    def __str__(self):
        return self.name

    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td>"%(self.name, self.dept, self.family)

    def as_table_header(self):
        return "<th>Name</th><th>Dept</th><th>Family</th>"


    def display_name(self, request):
        return "Raw Material Group"


class RGroupForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(RGroupForm, self).__init__(*args, **kwargs)

    class Meta:
        model=RGroup
        exclude=()

# List of actual usable materials baed on which formulation recipe if created.
class Rcode(MyModel):
    _classname="Rcode"
    rgroup=models.ForeignKey(RGroup)
    rname=models.CharField(max_length=60)
    UNIT_CHOICES=(('GM','Grams'),('KG','Kilograms'),('LT','Litres'),('NO','Numbers'))
    unit=models.CharField(max_length=2,choices=UNIT_CHOICES)
    plant=models.ForeignKey('es.Plant',blank=True,null=True)  #some material belong to an area
    rcd=models.CharField(max_length=6,blank=True,null=True)

    def __str__(self):
        return self.rname

    def av(self):
        rid=self.id
        return self.rbatch_set.raw("select a.id,a.rcode_id_id,a.quantity,sum(b.quantity) as used,(a.quantity-sum(b.quantity)) as bal from mm_rbatch a,mm_rsr b where a.rcode_id_id=%s and a.id=b.rbatch_id_id group by a.id having a.quantity>used",[rid])

    def as_table(self):
        return "<td>%s</td>"%(self.rname)

    def as_table_header(self):
        return "<th>Name</th>"


    def display_name(self, request):
        if self.rgroup_id:
            return "Packing for " + self.rgroup_id
        return "Packing"


class RcodeForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(RcodeForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Rcode
        exclude=("rgroup",)


# Movement type whch reflect trnsaction type { say purchase| consumption| loss | transfer etc.)
class Mtype(MyModel):
    _classname="Mtype"
#    USAGE_CHOICES=(("O","Opening Balance"),("P","Purchase"),("M","Miscellaneous"),("R","Reserved"))
    mtype=models.PositiveIntegerField(primary_key=True)
    description=models.CharField(max_length=20,null=True)


    def as_table(self):
        return "<td>%s</td>"%(self.mtype)

    def as_table_header(self):
        return "<th>Name</th>"


    def display_name(self, request):
        return "Movement Type"



class MtypeForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(MtypeForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Mtype
        exclude=()


# Single purchase bill header details 
class Purchase(MyModel):
    supplier=models.ForeignKey(Supplier)
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
    ismodvat=models.BooleanField(default=False)
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

# Purchase item batch details [including quality status say purity etc]
class Rbatch(models.Model):
    purchase=models.IntegerField(null=True,blank=True)
    rcode=models.ForeignKey(Rcode)
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
    ismodvat=models.BooleanField(default=False)
    purity=models.DecimalField(max_digits=12, decimal_places=2,default=1)
    ispass=models.BooleanField(default=False)  #Pass or fail
    mfrr=models.CharField(max_length=40,blank=True,null=True)
    mfgdate=models.DateField(null=True,blank=True)
    lst=models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)
    cst=models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)
    expiery=models.DateField(null=True,blank=True)

    def _bal(self):
        return 10

    balance = property(_bal)


#quality data shall flow from existing system


#  Material inventory transaction register- all incoming and outgoing
class Rsr(models.Model):
    fstype=models.ForeignKey("pp.Fstype",null=True,blank=True)
    tab_tp=models.CharField(max_length=1,blank=True,null=True)
    date=models.DateField(default=datetime.date.today())
    rbatch=models.ForeignKey(Rbatch)
    mtype=models.ForeignKey(Mtype)   #movement type
    quantity=models.DecimalField(max_digits=12, decimal_places=4)
    areato=models.ForeignKey('es.Plant', blank=True,null=True)

class Test(models.Model):
      packing=models.ForeignKey(Packing,blank=True,null=True)
      test=models.CharField(max_length=100)



