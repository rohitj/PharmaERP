from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db import transaction
from django.db.models import Q
import datetime

def aboutus(request):
  content = "<strong>Rohit Jain</strong><br />Graduate Student, Computer Science, Purdue University<br />B Tech, Computer Science, IIT Kanpur.<br />website : http://rohitj.net<br />mail at : jdb@rohitj.net <br />"
  return render_to_response('index.html', {'title': "About Us", 'header': "About Us", 'nonform': content})

def help(request):
  content = "coming soon ..........."
  return render_to_response('index.html', {'title': "Help", 'header': "Help", 'nonform': content})

def run(request):
  if request.user.is_authenticated():
    return render_to_response('menu.html', {'onlineinfo': request.user.username, 'title': "Welcome to Office Management", 'header': "Welcome to Office Management"})
  return render_to_response('menu.html', {'title': "Welcome to Service Management System", 'header': "Welcome to Service Management System"})

