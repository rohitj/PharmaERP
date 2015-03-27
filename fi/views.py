from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
def test(request, year):
    return HttpResponse("Hello World f FI  % s." % request.path )
# Create your views here.
