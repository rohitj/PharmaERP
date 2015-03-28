from django.db import models
from django.forms import ModelForm
from django import forms
import datetime

#------------------------------------------------------------------------------------------------
#  MM Module:  Product & raw material | Stock register for both | Unit Mgt | Supplier & purchases
#------------------------------------------------------------------------------------------------

# Test model
class Book(models.Model):
    name = models.CharField(max_length=200)

# Supplier master
class Sup(models.Model):
    code=models.OneToOneField('fi.Code',primary_key=True)
    stno=models.CharField(max_length=30,null=True,blank=True,verbose_name="Sale Tax No")
    eccno=models.CharField(max_length=20,null=True,blank=True)
    identity=models.CharField(max_length=10,null=True,blank=True)
    active=models.BooleanField(default=True)

    def __str__(self):
        return '%s' % (self.code)

# Product group master [ Each item indicate one product line]
class Pgroup(models.Model):
    groupname = models.CharField(max_length=60)
    bs_cat=models.CharField(max_length=10,null=True,blank=True)
    rmarea_id=models.ForeignKey('es.Rmarea')
    isactive=models.BooleanField(default=True)

    def required(self,b,dep):
         from pf2.pp.models import Rmrecipemaster,Rmrecipe
         qty=b.batchsize()

         if dep=="RM":
             q=Rmrecipemaster.objects.filter(pgroup_id=self, fdate__lt= datetime.date.today(), tdate__gt=datetime.date.today())
             f= q[0].rmrecipe_set.all().extra(select={"treq":0L,"alloted":0L})
             for item in f:
                item.treq=item.cal(qty)
                item.nreq=0.00
         else:
             q=Pmrecipemaster.objects.filter(pgroup_id=self, fdate__lt= datetime.date.today(), tdate__gt=datetime.date.today())
             f= q[0].pmrecipe_set.all()

         return f

    def __str__(self):
        return "%s" % (self.groupname)
		
# Indicates one product packing within a product line [ will have individual formulation]
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

# List of supplier of finished product- Pharmasynth sometimes buy finshed product and market those product. Not to be used.
class Psup(models.Model):         #product suppllier
    code=models.OneToOneField('fi.Code',primary_key=True)

# Not to be used.
class Recno(models.Model):
    psup_id=models.ForeignKey(Psup)
    date=models.DateField('receipt date')
# Not to be used.
class Pbatch(models.Model):
    recno_id=models.ForeignKey(Recno)
    batchname=models.CharField(max_length=20)
    expiery=models.DateField('expiery date')

# Finished goods store items.
class Psr(models.Model):
    vno_id=models.IntegerField()  #ForeignKey(Vno,blank=True,null=True)
    pack_id=models.ForeignKey(Packing)
    pbatch_id=models.ForeignKey(Pbatch)
    fullcases=models.IntegerField(null=True,blank=True)
    looseqty=models.IntegerField(null=True,blank=True)
    quantity=models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return ' '

# Units -  to be extended with additional fields 
class Unit(models.Model):
    name=models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.name

# Dimension master say VOLUME MASS DENSITY etc.
class Quantity(models.Model):
    name=models.CharField(max_length=10)
    unit=models.ForeignKey(Unit)

    def __str__(self):
        return self.name

# Unit conversion interface from one unit to another
class Uc(models.Model):
    quantity_id=models.ForeignKey(Quantity)
    u1=models.ForeignKey(Unit,related_name='fromunit')
    u2=models.ForeignKey(Unit,related_name='tounit')
    factor=models.DecimalField(max_digits=10,decimal_places=4)

    def __str__(self):
        return "%s %s " % (self.u1 + "-->"+  self.u2)

#  Material group-  class of input materials
class Rgroup(models.Model):
    groupname = models.CharField(max_length=60)
    DEPT_CHOICES=(('RM','Raw Material'),('PM','Packing Material'))
    dept=models.CharField(max_length=2,choices=DEPT_CHOICES)
    family=models.CharField(max_length=6,blank=True,null=True)
    def __str__(self):
        return self.groupname

# List of actual usable materials baed on which formulation recipe if created.
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

# Movement type whch reflect trnsaction type { say purchase| consumption| loss | transfer etc.)
class Mtype(models.Model):
#    USAGE_CHOICES=(("O","Opening Balance"),("P","Purchase"),("M","Miscellaneous"),("R","Reserved"))
    mtype=models.PositiveIntegerField(primary_key=True)
    description=models.CharField(max_length=20,null=True)

# Single purchase bill header details 
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

# Purchase item batch details [including quality status say purity etc]
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

#  Material inventory transaction register- all incoming and outgoing
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



