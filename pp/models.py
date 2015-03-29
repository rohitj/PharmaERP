from django.db import models
from django.db import models
from django.forms import ModelForm
from django import forms
import datetime
from django.db.models import Avg, Max, Min, Count,Sum
from django.shortcuts import render_to_response

#------------------------------------------------------------------------------------------------
#	PP Module:	Production planning model contains Sales Order | Formulation |  Production Batch
#-------------------------------------------------------------------------------------------------

# Raw material recipe master
class Rmrecipemaster(models.Model):
    pgroup_id=models.ForeignKey('mm.Pgroup')
    fdate=models.DateField('effective from')
    tdate=models.DateField()

    def __str__(self):
        return '%s %s %s %s' % (self.pgroup_id,self.fdate,'to',self.tdate)

# Packing material recipe master
class Pmrecipemaster(models.Model):
    packing_id=models.ForeignKey('mm.Packing')
    fdate=models.DateField('effective from')
    tdate=models.DateField()

    def __str__(self):
        return '%s %s %s %s' % (self.packing_id,self.fdate,'to',self.tdate)

# Raw material used as : sometimes rcodes names are used differently in recipe [say sodium chloride called as (Salt as binder)
class Rcodeas(models.Model):
    rcode=models.ForeignKey('mm.Rcode')
    name=models.CharField(max_length=40)


# Version of RM recipe
class Rmrecipe(models.Model):
    rmrecipemaster_id=models.ForeignKey(Rmrecipemaster)
    rcode_id=models.ForeignKey('mm.Rcode')
    rcodeas_id=models.ForeignKey(Rcodeas)
    TAB_CHOICES=(('L','Lubrication'),('G','Granulation'),('P','Paste Making'),(' ','None'))
    tab_tp=models.CharField(max_length=1,choices=TAB_CHOICES)
    claim= models.CharField(max_length=20)
    fraction=models.DecimalField(max_digits=10, decimal_places=4)
    overage=models.DecimalField(max_digits=10, decimal_places=2)
    unit=models.ForeignKey('mm.Unit')
    witem=models.BooleanField(default=True)     #should include in total weight
    isactive=models.BooleanField(default=True)  #expiery check or not
    roff=models.IntegerField(default=4)

    def cal(self,qty):
        return round(self.fraction*qty*(100+self.overage)/100,self.roff)


# Version of PM recipe
class Pmrecipe(models.Model):
    pmrecipemaster_id=models.ForeignKey(Pmrecipemaster)
    rcode_id=models.ForeignKey('mm.Rcode')
    claim= models.CharField(max_length=20)
    fraction=models.DecimalField(max_digits=10, decimal_places=4)
    overage=models.DecimalField(max_digits=10, decimal_places=2)
    roff=models.IntegerField(default=4)				# round off decimals

    def required(self,qty):
        return qty*self.fraction*(100+self.overage)/100


# Sale is done through some known transporters- so a master.
class Ptransport(models.Model):
      name=models.CharField(max_length=40)
      rmarea_id=models.ForeignKey('es.Rmarea')

      def __str__(self):
          return self.name


# List of key persons whose sale order we are processing. They can place orders online.
class Contacts(models.Model):                  # loan licensing
    name=models.CharField(max_length=40)
    rmarea_id=models.ForeignKey('es.Rmarea')  # optional so avoided the foreignkey
    email1=models.CharField(max_length=40)
    email2=models.CharField(max_length=40)
    email3=models.CharField(max_length=40)

    def __str__(self):
        return '%s %s ' % (self.name, self.rmarea_id)


# Sale orders master
from django.contrib.auth.models import User
class Pordermaster(models.Model):
    rmarea_id=models.ForeignKey('es.Rmarea')
    orno=models.CharField(max_length=40,null=True,verbose_name="Customer Order No")
    date=models.DateTimeField()
    transport_id=models.ForeignKey(Ptransport,blank=True,null=True)
    who=models.ForeignKey(Contacts)
    MMODE_CHOICES=(("W","Online"),("T","Telephone"),("M","Mail"),("O","Others"))
    mmode=models.CharField(max_length=1,default="A",choices=MMODE_CHOICES,verbose_name="Mode")
    userid=models.ForeignKey(User)

    def __str__(self):
        return '%s %s' % (self.rmarea_id,self.date)
    class Meta:
        verbose_name="Production Order"
        unique_together=("rmarea_id","date")

# Sale orders details
class Porder(models.Model):
    pordermaster_id=models.ForeignKey(Pordermaster)
    packing_id=models.ForeignKey('mm.Packing',verbose_name="Product Packing")
    quantity=models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    mrp=models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    rate=models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    actual=models.DecimalField(max_digits=10, default=0,decimal_places=2,blank=True)
    edd=models.DateField(verbose_name="Expected Date")
    tdd=models.DateField(verbose_name="Target Date",default=datetime.date.today())  # target date of delivery
    STATUS_CHOICES=(("O","Open"),("H","Hold"),("C","Consolidate"),("R","Reject"))
    status=models.CharField(max_length=1,default="C",choices=STATUS_CHOICES)

    def test(self):
        already_planned = MbatchPo.objects.filter(porder_id=self).aggregate(sum=Sum("quantity"))
        if not already_planned['sum']:
            planned=0
        else:
            planned=already_planned['sum']
        return self.quantity - planned

    def __str__(self):
        return '%s %s %s' % (self.pordermaster_id,self.packing_id, self.test())

# May be used later
class Mplanmaster(models.Model):
    rmarea_id=models.ForeignKey('es.Rmarea')
    fdate=models.DateField()
    tdate=models.DateField()

# May be used later
class Operation(models.Model):
    pgroup_id=models.ForeignKey('mm.Pgroup')
    srno=models.IntegerField()
    operation=models.CharField(max_length=20)

# May be used later
class Phase(models.Model):
    pgroup_id=models.ForeignKey('mm.Pgroup')
    srno=models.IntegerField()
    phase=models.CharField(max_length=20)


# Batch planned 
class Mbatch(models.Model):
    fsno=  models.CharField(max_length=10)			# systematic way of batch numbers while batchno is the text of FSNO
    batchno=models.CharField(max_length=10)
    pgroup_id=models.ForeignKey('mm.Pgroup')
    rmrecipemaster_id=models.ForeignKey(Rmrecipemaster,blank=True,null=True)
    pmrecipemaster_id=models.ForeignKey(Pmrecipemaster,blank=True,null=True)
    date_processing=models.DateField(blank=True,null=True)
    date_relasing=models.DateField(blank=True,null=True)
    date_completion=models.DateField(blank=True,null=True)   #finalize costing here and update cost module
    expiery=models.IntegerField(null=True)
    PRIORITY_CHOICES=(('A','Normal'),('B','Urgent'),('C','Immediate'))
    priority=models.CharField(max_length=1,default="A",choices=PRIORITY_CHOICES,null=True)
    isrelased=models.BooleanField(default=False)
    STAGE_CHOICES=(('A','Planning'),('B','Processing'),('C','Transfer'),('D','Complete'))
    phase=models.ForeignKey(Phase,blank=True,null=True)			# # May be used later
    operation=models.ForeignKey(Operation,blank=True,null=True)	# # May be used later
    stage=models.CharField(max_length=1,choices=STAGE_CHOICES,blank=True,null=True)

    def batchsize1(self):
        from django.db.models import Sum
        return self.MbatchPo__set.aggregate(total=Sum('quantity'))['total']

    def distt(self):
        from PharmaERP.mm.models import Packing
        dt=MbatchPo.objects.values("porder_id__packing_id").annotate(sum=Sum("quantity"))
        s=0
        for d in dt:
            f=Packing.objects.get(["porder_id__packing_id"]).fst(d['sum'])
            s+=d["sum"]
        return s

    def batchsize(self):
        from PharmaERP.mm.models import Packing
        dt=MbatchPo.objects.filter(mbatch_id=self).values("porder_id__packing_id").annotate(sum=Sum("quantity"))
        s=0
        for d in dt:
            p= Packing.objects.get(id=d["porder_id__packing_id"])
            if p:
               f=  d["sum"] * p.cfactor
               s =s+f
        return s

    def newrmfs(self,mode="I"):
        fs=Fstype(mbatch_id=self,fstype=mode,dept="RM",status=0)  #status 0 is new un-updated
        r=self.required("RM")
        c=Fs()
        c.obatch=self
        c.ofs=fs
        c.req=r
        c.bsize=self.batchsize()
        c.getfs()
        return c

    def required(self,dep):
        if dep=="RM":
            r=self.pgroup_id.required(self,"RM")
        else:
            r=self.pgroup_id.required(self,"PM")
        return r

    def __str__(self):
        return '%s %s %s ' % (self.fsno,self.pgroup_id,self.batchsize())

# Production batch PLanning linked sale orders
class MbatchPo(models.Model):
    mbatch_id=models.ForeignKey(Mbatch)
    porder_id=models.ForeignKey(Porder)
    quantity=models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    issquare=models.BooleanField()				# means close the sale order ith this qty.

    def __str__(self):
        return '%s %s' % (self.porder_id,self.quantity)


# Packing details of each batch planned
class Distt(models.Model):
    mbatch_id=models.ForeignKey(Mbatch)
    packing_id=models.ForeignKey('mm.Packing')
    quantity=models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    produced=models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    unticost=models.DecimalField(max_digits=10, decimal_places=2,blank=True)		# cost of unit production shall be updated later.

    def __str__(self):
        return '%s %s %s ' % (self.mbatch_id,self.packing_id,self.quantity)

# A production batch contains several material issue requests. One such request may contain several materials in it. This is master of that
class Fstype(models.Model):
    mbatch_id=models.ForeignKey(Mbatch)
    FSTYPE_CHOICES=(('I','Issue'),('R','Return'))
    fstype=models.CharField(max_length=2,choices=FSTYPE_CHOICES)
    date=models.DateField(null=True)
    DEPT_CHOICES=(('RM','Raw Material'),('PM','Packing Material'))
    dept=models.CharField(max_length=2,choices=DEPT_CHOICES)
    islocked=models.BooleanField()							# locked the quantity for this batch.
    status=models.IntegerField()


    def __str__(self):
        return '%s %s' % (self.mbatch_id,self.dept)

    def pmfs_issue(self,mode="I"): # mode is issue or return flow sheet.
        qty=self.mbatch_id.batchsize()
        ds=self.mbatch_id.distt_set.all()
        dl=list([])
        for d in ds:
            f=Pmrecipemaster.objects.filter(packing_id=d.packing_id,fdate__lt=self.date,tdate__gt=self.date)
            if f:
                dl.extend(f[0].recipe_set.all())
        return qty

        class Meta:
            Isnew=True

# TV stands for transfer vouche- Each batch can have several output set- one such set may have X qty of product produced.
class Tvmaster(models.Model):
    date=models.DateField(null=True)

# Details of one TVmaster.
class Tv(models.Model):
    tvmaster_id=models.ForeignKey(Tvmaster)
    distt_id=models.ForeignKey(Distt)
    quantity=models.DecimalField(max_digits=10, decimal_places=0)


class Fs(object):
    req=None
    ofs=None
    obatch=None
    dept="RM"
    status=0
    mode="I"
    bsize=0
    lfs=None

    def getfs(self):
        from PharmaERP.mm.models import Rsr
        from PharmaERP.mm.models import Rbatch
        from PharmaERP.mm.models import Mtype
        from decimal import Decimal
        qr=self.req
        pl=[]
        for r in qr:
            nreq=Decimal(r.treq)
            qav=r.rcode_id.av()
            for a in r.rcode_id.av():
                q=min(a.bal,nreq)
                pl.append(Rsr(fstype_id=self.ofs,rbatch_id=Rbatch.objects.get(id=a.id),quantity=q,mtype_id=Mtype.objects.get(mtype=261)))
                nreq=nreq-q
                if nreq<=0.00:
                   break
        self.lfs=pl
        return None

