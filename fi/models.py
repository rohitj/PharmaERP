from django.db import models
from django.forms import ModelForm
from es.models import Code

#------------------------------------------------------------------------------------------------
#  FI Module:  Ledger account head and entry alongwih bill allocation
#------------------------------------------------------------------------------------------------

class Book(models.Model):
    name=models.CharField(max_length=60)

# Ledger heads including customer / suplier / employee/ others 
#class Code(models.Model):
#    name=models.CharField(max_length=60)
#    address=models.CharField(max_length=60,null=True,blank=True)
#    SUPERCLASS_CHOICES=(("ASSETS","ASSETS"),("LIABILITIIES","LIABILITIIES"),("EXPENDITURE","EXPENDITURE"))
#    superclass= models.CharField(max_length=15,choices=SUPERCLASS_CHOICES,null=True,blank=True)
#    GCLASS_CHOICES=(("CUS","CUSTOMER"),("SUP","SUPPLIER"),("REP","REPRESENTATIVE"),("EMP","Employee"),("CON","Contacts"),("PSP","Product Supplier"),("OTH","Others"))
#    gclass=models.CharField(max_length=3,choices=GCLASS_CHOICES,null=True,blank=True)
#    sclass=models.CharField(max_length=3,choices=GCLASS_CHOICES,null=True,blank=True)
#    ssclass=models.CharField(max_length=3,choices=GCLASS_CHOICES,null=True,blank=True)
#    schedule=models.CharField(max_length=15,null=True,blank=True)
#
#    def __str__(self):
#        return "%s %s %s %s" % (self.name, self.superclass, self.gclass,self.test())
#
#    def test(self):
#         return "OK"
#    class Meta:
#         verbose_name = "Account Head"


class LedEntry(models.Model):
    pass

# All financial transactions in ledger
class Led(models.Model):
    doctype=models.CharField(max_length=2) # 
#    nature=models.CharField(max_length=1) # 
    vno=models.ForeignKey('sd.VoucherNo',blank=True,null=True)
    pur=models.ForeignKey('mm.Purchase',blank=True,null=True)
#    vno=models.IntegerField()
    book=models.ForeignKey(Book)
    code=models.ForeignKey(Code)
    date=models.DateField()
    subvno=models.IntegerField()
    amount=models.DecimalField(max_digits=12, decimal_places=2)
    refdoc=models.IntegerField()

# Billwise paymnet allocation
class Pay(models.Model):
    bill_id=models.IntegerField()             # a led id for bill
    pay_id=models.ForeignKey(Led)
    amount=models.DecimalField(max_digits=12, decimal_places=2)
    discount=models.DecimalField(max_digits=12, decimal_places=2)
    interest=models.DecimalField(max_digits=12, decimal_places=2)

