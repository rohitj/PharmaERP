from django.db import models

#------------------------------------------------------------------------------------------------
#from fi.models import Code
#from es.models import Pageno

class Cust(models.Model):
    code=models.OneToOneField('fi.Code',primary_key=True)
    active=models.BooleanField(default=1)
    pageno_id=models.ForeignKey('es.Pageno')

    def save(self,*args,**kwargs):
        if self.address=="A":
            return
        else:
            super(Cust,self).save(*args,**kwargs)

    def __str__(self):
        return '%s' % (self.code)

#from mm.models import Packing
class Plist(models.Model):
    packing_id=models.ForeignKey('mm.Packing')
    CAT_CHOICES=(('S1','S1'),('S2','S2'),('S3','S3'),('S4','S4'),('S5','S5'),('S6','S6'),('S7','S7'),('S8','S8'))
    category=models.CharField(max_length=2,default='S1',choices=CAT_CHOICES)
    date = models.DateField('effective from')
    price=models.DecimalField(max_digits=10, decimal_places=2)

#    class Meta:
       #unique_together = (('packing_id','category' ),)
    def __str__(self):
        return self.category

class Vno(models.Model):
    date = models.DateField('bill date')
    cust_id=models.ForeignKey(Cust)
    ino=models.IntegerField(unique_for_year="date")

    def __str__(self):
        return '%s  %s' % (self.date,cust_id)


#------------------------------------------------------------------------------------------------
