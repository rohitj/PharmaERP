from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from es.models import *
# Create your views here.
def test(request, year):
    return render_to_response('test.html')


def new_client(request):
    messages = []
    if request.method == 'POST':
      form = CltForm(request, request.POST, request.FILES)
      if form.is_valid():
        form.save(request)
        return HttpResponseRedirect("./?message='Form Saved'")
    else:
      message = request.GET.get('message', '')
      if message:
        messages = [message,]
      form = CltForm(request)
    return render_to_response('index.html', {'onlineinfo': request.user.username, 'title': "New Client", 'header': "New Client", 'form': form, 'messages': messages})



def new_plant(request):
    messages = []
    if request.method == 'POST':
      form = PlantForm(request, request.POST, request.FILES)
      if form.is_valid():
        form.save(request)
        return HttpResponseRedirect("./?message='Form Saved'")
    else:
      message = request.GET.get('message', '')
      if message:
        messages = [message,]
      form = PlantForm(request)
    return render_to_response('index.html', {'onlineinfo': request.user.username, 'title': "New Plant", 'header': "New Plant", 'form': form, 'messages': messages})


def list_plant(request):
    pageno = 1
    if request.GET.get('pageno'):
        pageno = int(request.GET.get('pageno'))

    results = Plant.objects.all();

    next = None
    prev = None
    if pageno > 1:
        prev = pageno-1

    results = results.all()[(pageno-1)*RESULT_PER_PAGE:(pageno)*RESULT_PER_PAGE + 1]
    if len(results) > RESULT_PER_PAGE:
        next = pageno + 1
    results = results[0:RESULT_PER_PAGE]

    return render_to_response('list.html', {'onlineinfo': request.user.username, 'title': "Plants", 'header': "Plants", 'results':results, 'pageno':pageno, 'prev':prev, 'next':next})
