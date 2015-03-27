# Create your views here.
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import render_to_string
from django import forms
from readonly import *

from django.utils.functional import curry
from pf2.mm.models import *
from pf2.pp.models import *
from pf2.sd.models import *
from pf2.es.models import *
from pf2.fi.models import *
from pf2.mm.forms import *
from pf2.pp.forms import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.utils import simplejson

import datetime
from django.contrib import admin
from django.template.context import RequestContext
@csrf_protect

#-------------------------------------------------------------------------------

def newfs(request):
    b=Mbatch.objects.get(id=1)
    o=b.newrmfs() # o is custom object of Fs class defined in pp.models file
    return render_to_response("workin-ajax.html",{'obatch':o,'heading1':"New Flow Sheet"})

admin.site.add_action(newfs)


def newfs1(requet):   #test


    b=Mbatch.objsects.get(id=1)
    o=b.newrmfs() # o is custom object of Fs class defined in pp.models file
    return render_to_response('newfs-test.html',{'obatch':o,'heading1':"New Flow Sheet"})

admin.site.add_action(newfs)


def batchlist(request):

    if request.POST:
        head="Post"
    else:
        head="Get"

    b=Mbatch.objects.all()
#    o=b.newrmfs() # o is custom object of Fs class defined in pp.models file
    return render_to_response('batchlist2.html',{'obatch':b,'heading1':head},context_instance=RequestContext(request))

admin.site.add_action(newfs)

def batchlist1(request):
    data=request.POST
    b=Mbatch.objects.all()
#    o=b.newrmfs() # o is custom object of Fs class defined in pp.models file
    return render_to_response('ajax.html')


def xhr_test(request):
    if request.is_ajax() and request.method=="POST" :
        data1=serializers.serialize('json',Packing.objects.all())
#       q=request.POST["num"]
        q = "Hello AJAX"
    else:
        q = "Hello"

    return HttpResponse(q,mimetype='text/plain')#'application/json')


def prod(request):
    if request.is_ajax():
        area=request.POST["area"]
        data1=serializers.serialize('json',Pgroup.objects.filter(rmarea_id=area))
#       q=request.POST["num"]
        q = "Hello AJAX"
    else:
        q = "Hello"

    return HttpResponse(data1,mimetype='application/json')



def xhr_test1(request):
    if request.is_ajax():
        data=serializers.serialize('json',Packing.objects.all())
        message = "Hello AJAX"
    else:
        message = "Hello"
    return HttpResponse(message)

def rb():
    m=Mtype.objects.get(mtype=301)
    r=Rcode.objects.get(id=6)
    rec=Rbatch(rcode_id=r,batchno="B1",trno="T2",mtype_id=m,quantity=250,ispass=True,ismodvat=True)
    rec.save()
    return rec

def rc():
    m=Mtype.objects.get(mtype=641)
    r=Rbatch.objects.get(id=2)
    rec=Rsr(rbatch_id=r,mtype_id=m,quantity=50,date=datetime.date.today())
    rec.save()
    return rec

def newpo(request,*arg):
    import pdb;pdb.set_trace()
    no=arg[0]
    area=Rmarea.objects.get(pk=no)
    action= request.POST.get("action")

    if request.method=='POST' and action=="Details":
        form=PoForm(request.POST)

        if form.is_valid():
            f=form.save(commit=False)
            f.rmarea_id=Rmarea.objects.get(id=arg[0])
            f.save()
            return render_to_response('/pp/msg.html',{'message':"Data Saved"} )
        else:
            return render_to_response('error.html',{'message':"Invalid Data"} )
    else:

        om=Pordermaster(rmarea_id=area,mmode="Telephone",date=now,who=1)
        poform=PoForm(instance=om,)

    return render_to_response('newpo.html',{'form':poform,'heading1':area.name})
#    return HttpResponseRedirect('/admin/pp/pordermaster/add/')

def my_jason_view(request):
    data=serializers.serialize('json',Packing.objects.all())
    return HttpResponse(data,mimetype='application/json')

def packcount(request):
    if request.method == 'GET':
        GET=request.GET
        pk=GET[u'pcd']
        results={'count':3}
#    json1=simplejson.dump(results)
    return HttpResponse(json1,mimetype='application/json')

def newdistt(request,*arg):
    no=arg[0]
#    request.session['message']='Hello view2!'
#    return HttpResponseRedirect(reverse('view2'))
    try:
        bid=Mbatch.objects.get(pk=no)
    except (KeyError,Mbatch.DoesNotExist):
        msg="Keyerror"
        return render_to_response('error.html',{'message':msg} )
    else:
        pcd=bid.pgroup_id

        count=pcd.packing_set.count()
        ps=pcd.packing_set.all()
        DisttFormset=formset_factory(MyForm,extra=count)

    if request.method=='POST':
        data=request.POST
        formset=DisttFormset(request.POST)
        if formset.is_valid():
            i=-1
            for pack in ps:
                i=i+1
                q=bid.distt_set.filter(packing_id=pack.id)
                if q:
                    p=Distt.objects.get(packing_id=q[0].packing_id)
                    p.quantity=formset[i].cleaned_data['quantity']
                    p.save()
                    msg = "Already exists and modified,,,"
                else:
                    d=Distt(mbatch_id=bid,packing_id=pack,quantity=100)
                    d.save()
                    msg="Saved"
            return render_to_response('error.html',{'message':msg} )
        else:
            msg = "Invalid distt data"
            return render_to_response('error.html',{'message':msg} )
    else:
        initvalues=[]
        q = bid.distt_set.all()
        for pack in ps:
            r=q.filter(packing_id=pack.id)
            if r:
                initvalues.insert(0,{'quantity':r[0].quantity})
            else:
                initvalues.insert(0,{'quantity':0})

        formset = DisttFormset(initial=initvalues)
        return render_to_response('test.html',{'formset':formset,'ps':ps,'pcd':pcd,'fsno':bid})

def newdistt2(request):
    no=request.POST['pcode']
    pcd=Pgroup.objects.get(pk=no)
    count=pcd.packing_set.count()
    ps=pcd.packing_set.all()
    form=make_distt_form(pcd)
    pfactor=Packing.objects.filter(pgroup_id=pcd)
    nos=pfactor.count()
    DisttFormset =formset_factory(form=form)#formset_factory(DisttForm, extra=2)
#    mydic= pfactor.values_list("packing_id","unitppack",)
#    my_data={"form-TOTAL_FORMS":nos,"form-INITIAL_FORMS":0,"form-MAX_NUM_FORMS":nos}
#    i=0
#    for  o in pfactor:
#        var="form-"& i & "-packing_id"
#        my_data[var]= i+1
#        my_data["form-"& i & "-quantity"]= 0
#        my_data["form-"& i & "-units"]= 0
#        my_data["form-"& i & "-unitQty"]= 0
#        i=i+1
    my_data={"form-TOTAL_FORMS":nos,"form-INITIAL_FORMS":0,"form-MAX_NUM_FORMS":nos,"form-0-packing_id":1, "form-1-packing_id":2,"form-0-quantity":0,"form-1-quantity":0,"form-0-units":100,"form-1-units":100,"form-0-unitQty":1,"form-1-unitQty":100,}
    formset=DisttFormset(data=my_data)
#    formset =modelformset_factory(Distt, form=form,extra=2)#formset_factory(DisttForm, extra=2)
    html = render_to_string( 'distt.html', {'formset':formset,'pfactor':pfactor})
    res = {'html': html}

    return HttpResponse( html,{'pfactor':pfactor},mimetype='text/plain' )

def make_distt_form(pcd):
    class DisttForm(forms.ModelForm):
        quantity=forms.CharField(max_length=15,widget=forms.TextInput(attrs={'class':'btclass'}))
        units=forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'myclass'}))
        packing_id = forms.ModelChoiceField(queryset=Packing.objects.filter(pgroup_id=pcd))
        unitQty=forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class':'myclass','size':10}))

        def __init__(self,*args,**kwargs):
            super(DisttForm,self).__init__(*args,**kwargs)
            instance=getattr(self,'instance',None)
            if instance and instance.id:
                self.fields['units'].widget.attrs['readonly']=True
                self.fields['units'].value='200'
        def clean_units(self):
            return self.instance.units

        class Meta:
            model=Distt
            exclude=('id','mbatch_id','produced','unticost',)
    return DisttForm
#-----------------------------------------------------------------------------------------
from forms import BatchForm
def newbatch(request):
    if request.method=='POST':
        action= request.POST.get("action")
        if action=="Save":
            form=BatchForm(request.POST,request.FILES)
            form.save()
            d1=request.POST.get("batch")
#            d2=request.POST.get("distt")
            if form.is_valid():
                form.save()
                msg="Saved..."
              #batch=form.cleaned_data['id']
            else:
                msg="Invalid data..." + d1['pgroup_id']
                return HttpResponse(msg,mimetype='text/plain' )
        else:
            msg="Could not reach action"
            return HttpResponse(msg,mimetype='text/plain' )
    else:
#        try:
#            r=Rmarea.objects.get(pk=1)
#            b=Mbatch.objects.get(pk=id)  #get_object_or_404(Mbatch,pk=id)
#        except (KeyError,Mbatch.DoesNotExist):
#            msg="Keyerror"
#            return render_to_response('error.html',{'message':msg} )
#        else:
        form = BatchForm()

        rform=RmareaForm()
        return render_to_response('newbatch.html',{'rform':rform,'form':form,'heading1':"New Batch"},context_instance=RequestContext(request))

def changebatch(request,id):
    if request.method=='POST':
        action= request.POST.get("action")
        if action=="Save":
            form=BatchForm(request.POST,request.FILES)

            if form.is_valid():
                form.save()
                msg="Saved..."
                #batch=form.cleaned_data['id']
            else:
                msg="Invalid data..."
                return HttpResponse(msg,mimetype='text/plain' )
        else:
            msg="Could not reach action"
            return HttpResponse(msg,mimetype='text/plain' )
    else:
    #        try:
    #            r=Rmarea.objects.get(pk=1)
    #            b=Mbatch.objects.get(pk=id)  #get_object_or_404(Mbatch,pk=id)
    #        except (KeyError,Mbatch.DoesNotExist):
    #            msg="Keyerror"
    #            return render_to_response('error.html',{'message':msg} )
    #        else:
        b=Mbatch.objects.get(pk=id)
        form = BatchForm(instance=b)
        rform=RmareaForm()

        return render_to_response('newbatch.html',{'rform':rform,'form':form,'heading1':"Change Batch"},context_instance=RequestContext(request))



def home(request):
    object_list=Pgroup.objects.all()
    return render_to_response('pg.html',{'object_list':object_list})

def details(request):
    p=Pgroup.objects.get(pk=object_id)
    c=p.packing_set.all()
    return render_to_response('pcode_detail.html',{'object':c[0],'check':object_id})

def plist(request,object_id):
    p=Plist.objects.get(pk=object_id)
    return render_to_response('pcode_detail.html',{'object':p})

def create(request):
    return render_to_response('pcodecreate.html',{'check',abc})

def error(request):
    return render_to_response('error.html',{'check',abc})

def pgroup(request):
    if request.method=='POST':
        form=PgroupForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/home/')
    else:
        form=PgroupForm()
    return render_to_response('pgroup1.html',{'form':form,})