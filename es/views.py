from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
def test(request, year):
    return render_to_response('test.html')
