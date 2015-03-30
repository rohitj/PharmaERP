from django.db import models
from es.models import *
from mm.models import *
#------------------------------------------------------------------------------------------------

# Finished goods store items.
class Psr(MyModel):
    vno=models.ForeignKey("sd.VoucherNo",blank=True,null=True)                 # Purchase voucher number
    packing=models.ForeignKey("mm.Packing")
    pbatch=models.ForeignKey("mm.Pbatch")                                        # Not to be used
    fullcases=models.IntegerField(null=True,blank=True)                     # Finished goods  full boxes in stock
    looseqty=models.IntegerField(null=True,blank=True)
    quantity=models.DecimalField(max_digits=10, decimal_places=0)
#    price

    def __str__(self):
        return ' '

class Customer(Code):
    _classname="Customer"
    active=models.BooleanField(default=1)
    pageno=models.ForeignKey(Pageno)

    def save(self,*args,**kwargs):
        if self.address=="A":
            return
        else:
            super(Customer,self).save(*args,**kwargs)

    def __str__(self):
        return '%s' % (self.name)

    def as_table(self):
        return "<td>%s</td><td>%s</td><td>%s</td>"%(self.name, self.active, self.pageno)

    def as_table_header(self):
        return "<th>Name</th><th>Active</th><th>PageNo</th>"



class CustomerForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)

    class Meta:
        model=Customer
        exclude=()


class Plist(MyModel):
    packing=models.ForeignKey(Packing)
    CAT_CHOICES=(('S1','S1'),('S2','S2'),('S3','S3'),('S4','S4'),('S5','S5'),('S6','S6'),('S7','S7'),('S8','S8'))
    category=models.CharField(max_length=2,default='S1',choices=CAT_CHOICES)
    date = models.DateField('effective from')
    price=models.DecimalField(max_digits=10, decimal_places=2)

#    class Meta:
       #unique_together = (('packing_id','category' ),)
    def __str__(self):
        return self.category

class VoucherNo(models.Model):
    date = models.DateField('bill date')
    cust=models.ForeignKey(Customer)
    ino=models.IntegerField(unique_for_year="date")

    def __str__(self):
        return '%s  %s' % (self.date,cust)


#------------------------------------------------------------------------------------------------
