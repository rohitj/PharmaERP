from pp.models import Pordermaster,Ptransport,Mbatch,Distt
from es.models import Plant
from mm.models import PGroup
from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget

class PoForm(ModelForm):
#    date=forms.DateField(widget=SelectDateWidget())
    class Meta:
        model=Pordermaster
        exclude=('plant','userid',)

class BatchForm(ModelForm):
    class Meta:
        model=Mbatch
#        fieldsets = ( (None, {'fields': (('pgroup_id','fssno','batch_no','priority','isrelased'), )        }),    )
        exclude={'stage','phase','operation','pmrecipemaster','rmrecipemaster','date_completion','isrelased',}

    def __init__(self,*args,**kwargs):
        super(BatchForm,self).__init__(*args,**kwargs)
        self.fields['date_processing'].widget=widgets.AdminDateWidget()




