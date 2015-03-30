from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.forms import *
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm as UserForm


RESULT_PER_PAGE = 20

def get_class( kls ):
  parts = kls.split('.')
  module = ".".join(parts[:-1])
  if module:
    m = __import__( module )
    for comp in parts[1:]:
      m = getattr(m, comp)
    return m
  else:
    return globals()[kls]



# classname is dependent on classname_dependent. For example, packing is dependent on pgroup
# classname: the class objects to be listed
# dependent_id: If the list of "class" objects needs to be restricted to only those objects which are dependent on "class_dependent" object with id "dependent_id", dependent_id is supplied. 

def newlist(request, classname, dependent_on=None, dependent_on_id=None, Type=0):
  Class = get_class("%s"%classname)
  tempobject = Class() #Just for getting create_url and display name among others
  class_objects = Class.objects
  if dependent_on:
    ClassDependent = get_class("%s"%dependent_on[1])
    tempclassdependent = ClassDependent.objects.get(id=dependent_on_id)
    class_objects = getattr(tempclassdependent, Class.__name__.lower()+"_set").all() #tempclassdependent.dependent(request, classname_nested)

  title = "%s"%(tempobject.display_name(request))
  header = "List of All %s"%(tempobject.display_name(request))

  extra_params = {}
  if dependent_on:
#    extra_params["dependent_on"] = dependent_on
    extra_params["dependent_on_id"] = dependent_on_id
  create_link_url = tempobject.create_url(request, extra_params)

  messages = []
  results, title, header = search_list(request, Class, class_objects, title, header)

  message = request.GET.get('message', '')
  if message:
    messages = [message,]

  pageno = 1
  if request.GET.get('pageno'):
    pageno = int(request.GET.get('pageno'))
  next = None
  prev = None
  if pageno > 1:
    prev = pageno-1
  results = results.all()[(pageno-1)*RESULT_PER_PAGE:(pageno)*RESULT_PER_PAGE + 1]
  if len(results) > RESULT_PER_PAGE:
    next = pageno + 1
  results = results[0:RESULT_PER_PAGE]

  return render_to_response('%s'%(tempobject.list_template(request)), {'onlineinfo': request.user.username, 'title': title, 'header': header, 'results':results, 'messages':messages, 'pageno':pageno, 'prev':prev, 'next':next, 'create_url':create_link_url, 'Class':Class, 'allow_search':"True", 'getVars':request.GET, 'link_template':tempobject.link_template(request)}, context_instance=RequestContext(request))



def list(request, classname, classname_oneonone=None, classname_nested=None, classname_dependent=None, dependent_id=None, Type=0):
  pageno = 1
  if request.GET.get('pageno'):
    pageno = int(request.GET.get('pageno'))

  Class = get_class("%s"%classname)
  tempobject = Class() #Just for getting create_url and display name among others
  ClassForm = get_class("%sForm"%classname)
  class_objects = Class.objects
  form = None
  form2 = None
  formset = None
  if classname_dependent:
    ClassDependent = get_class("%s"%classname_dependent)
    tempclassdependent = ClassDependent.objects.get(id=dependent_id)
    class_objects = tempclassdependent.dependent(request, classname_nested)
  if Class.is_create_allowed(request):
    messages = []
    if classname_nested:
      form, formset = nested(request, classname, classname_nested)
      if form ==None:
        return HttpResponseRedirect("./?message='Form Saved'")
    elif request.method == 'POST':
      form = ClassForm(request, request.POST, request.FILES)
      if form.is_valid():
        form.save(request)
        return HttpResponseRedirect("./?message='Form Saved'")
    else:
      message = request.GET.get('message', '')
      if message:
        messages = [message,]
      form = ClassForm(request)

  create_link_url = Class.create_url(request)

  title = "%s"%(tempobject.display_name(request))
  header = "List of All %s"%(tempobject.display_name(request))
  messages = []
  results, title, header = search_list(request, Class, class_objects, title, header)

  message = request.GET.get('message', '')
  if message:
    messages = [message,]

  next = None
  prev = None
  if pageno > 1:
    prev = pageno-1
  results = results.all()[(pageno-1)*RESULT_PER_PAGE:(pageno)*RESULT_PER_PAGE + 1]
  if len(results) > RESULT_PER_PAGE:
    next = pageno + 1
  results = results[0:RESULT_PER_PAGE]

  return render_to_response('%s'%(Class.template(request)), {'onlineinfo': request.user.username, 'title': title, 'header': header, 'results':results, 'messages':messages, 'pageno':pageno, 'prev':prev, 'next':next, 'Type':Type, 'create_url':Class.create_url(Type), 'Class':Class, 'allow_search':"True", 'getVars':request.GET, 'form':form, 'formset':formset, 'link_template':Class.link_template(request)}, context_instance=RequestContext(request))



def search_list(request, Class, class_objects, title, header):
  if request.method == 'GET' and request.GET.get('search'):
    query = request.GET.get('search')
    if query:
      title = "Search %s : '%s'"%(tempobject.display_name(request), query)
      header = "Search %s : '%s'"%(tempobject.display_name(request), query)
      items = query.split(',')
      results = class_objects.all()
      for item in items:
        item = item.strip()
        qset = Class.search_query(item)
        results = results.filter(qset)
      results = results.distinct()
    else:
      results = []
  else:
    results = class_objects
  return results, title, header


# classname: Name of the class whose object is to be created
# oneonone_forms: If there is a one-to-one field from classname to another class, oneonone is used to show form for the other class as well
#                 The oneonone_forms should be a list of tuples (fieldname, oneoneoneclassname), where fieldname is the name of the field of classname, and oneonone_classname is the classname of the field.
# dependent_on: If classname has a foreignkey, which has been picked. For example, in the page for station, there is a link to add pageno to station. In such case, the foreignkey field should not be picked by the user, but should be populated automatically at the time of form save.
#                 dependent_on is a tuple (fieldname, dependent_classname)
# dependent_on_id: If the classname is dependent, the id of the foreignkey object 
def newnew(request, classname, oneonone_forms=None, dependent_on=None, dependent_on_id=None, classname_nested=None, Type=0):
  Class = get_class("%s"%classname)
  tempobject = Class() #Just for getting create_url and display name among others
  dependent_obj = None
  if dependent_on:
    ClassDependent = get_class("%s"%dependent_on[1])
    dependent_obj = ClassDependent.objects.get(id=dependent_on_id)

  ClassForm = get_class("%sForm"%classname)
  form = None
  form2 = None
  formset = None
  if tempobject.is_create_allowed(request): # The user is allowed to create a new classname object
    messages = []
    if request.method == 'POST':
      print(request.POST)
      form = ClassForm(request, request.POST, request.FILES)
      if classname_nested:
        print("post nested")
        form, formset = nested(request, classname, classname_nested)
      if oneonone_forms:
        ClassOneOnOneForm = get_class("%sForm"%oneonone_forms[1])
        form2 = ClassOneOnOneForm(request.POST, request.FILES) #TODO: The passed parameter should also have "request" if the form was made in our code. Currently we are using UserCreationForm, so it doesnt take "request"
      valid = True
      if form:
        if not form.is_valid():
          print("form not valid")
          valid = False
      if form2:
        if not form2.is_valid():
          print("form2 not valid")
          valid = False
      if formset:
        if not formset.is_valid():
          print(formset.data)
          print("formset not valid")
          valid = False
      if valid:
        obj = form.save(commit=False)
        if oneonone_forms:
          a = form2.save()
          setattr(obj, oneonone_forms[0], a)
        if dependent_on:
          setattr(obj, dependent_on[0], dependent_obj)
        obj.save()
# TODO        obj.save_m2m()
        return HttpResponseRedirect("./?message='Form Saved'")
    else:
      message = request.GET.get('message', '')
      if message:
        messages = [message,]
      form = ClassForm(request)
      if classname_nested:
        form, formset = nested(request, classname, classname_nested)
      if oneonone_forms:
        ClassOneOnOneForm = get_class("%sForm"%oneonone_forms[1])
        form2 = ClassOneOnOneForm()


  title = "Create %s"%(tempobject.display_name(request))
  header = "Create %s"%(tempobject.display_name(request))
  messages = []

  message = request.GET.get('message', '')
  if message:
    messages = [message,]

  return render_to_response('new.html', {'onlineinfo': request.user.username, 'title': title, 'header': header, 'messages':messages, 'form':form, 'form2':form2, 'formset':formset}, context_instance=RequestContext(request))



def new(request, classname, Type=0):
  Class = get_class("%s"%classname)
  tempobject = Class()
  ClassForm = get_class("%sForm"%classname)
  if Class.is_create_allowed(request):
    messages = []
    if request.method == 'POST':
      form = ClassForm(request, request.POST, request.FILES)
      if form.is_valid():
        form.save(request)
        return HttpResponseRedirect("./?message='Form Saved'")
    else:
      message = request.GET.get('message', '')
      if message:
        messages = [message,]
      form = ClassForm(request)
    return render_to_response('index.html', {'onlineinfo': request.user.username, 'title': "New %s"%(Class.display_name(request)), 'header': "New %s"%(Class.display_name(request)), 'form': form, 'messages': messages})
  return HttpResponseRedirect("/")



def edit(request, classname, id=0, classname_nested=None, classname_dependent=None, dependent_id=0):
  Class = get_class("%s"%classname)
  tempobject = Class()
  ClassForm = get_class("%sForm"%classname)
  messages = []
  form=None
  formset=None
  if classname_nested and classname_dependent:
    ClassDependent = get_class("%s"%classname_dependent)
    tempdependent = ClassDependent.objects.get(id = dependent_id)
    ClassNested = get_class("%s"%classname_nested)
    myclassobject = Class.objects.filter(pgroup__id=dependent_id)
    if myclassobject:
      id = myclassobject[0].id
    else:
      myclassobject = Class()
      myclassobject.pgroup = tempdependent
      myclassobject.save()
      id = myclassobject.id

  tempclass = Class.objects.filter(id = id)[0]
  if tempclass.is_edit_allowed(request):
    if classname_nested:
      form, formset = nested(request, classname, classname_nested, id)
    elif request.method == 'POST':
      form = ClassForm(request, request.POST, request.FILES, instance=tempclass)
      if form.is_valid():
        form.save(request)
        return HttpResponseRedirect("./?message='Form Saved'")
    else:
      message = request.GET.get('message', '')
      if message:
        messages = [message,]

      form = ClassForm(request, instance=tempclass)

    return render_to_response(tempclass.edit_template(request), {'onlineinfo': request.user.username, 'title': "Edit %s"%tempobject.display_name(request), 'header': "Edit %s"%tempobject.display_name(request), 'form': form, 'messages': messages,'deleteinstance':tempclass, 'formset':formset})
  return HttpResponseRedirect("/")


def dependent(request, classname, classname_dependent, id=None):
  messages = []
  Class = get_class("pf.%s"%classname)
  ClassDependent = get_class("pf.%s"%classname_dependent)
  ClassDependentFormSet = inlineformset_factory(ClassDependent, Class, extra=1)
  tempclass = None
  if id:
    tempclass = Class.objects.get(pk=id)

  message = request.GET.get('message', '')
  if message:
    messages = [message,]
  if request.method == 'POST':
    formset = ClassDependentFormSet(request.POST, instance = tempclass)
    if formset.is_valid():
      formset.save()
      return HttpResponseRedirect("./?message='Form Saved'")
    else:
      messages.append("invalid form")
  else:
    if tempclass:
      formset = ClassDependentFormSet(instance=tempclass)
    else:
      formset = ClassDependentFormSet()

  return render_to_response(tempclass.edit_template(request), {'onlineinfo': request.user.username, 'title': classname_dependent, 'header': classname_dependent, 'formset': formset, 'messages': messages})


def delete(request, classname, id, Type=0):
  Class = get_class("pf.%s"%classname)
  tempclass = Class.objects.filter(id = id)[0]
  tempclass.delete()
  return HttpResponseRedirect("/")

def view(request, classname, id, Type=0):
  Class = get_class("%s"%classname)
  tempobject = Class()
  tempclass = Class.objects.filter(id = id)[0]
#  results = tempclass.dependent(request)
  return render_to_response(tempclass.view_template(request), {'onlineinfo': request.user.username, 'title': "View %s"%(tempobject.display_name(request)), 'header': "View %s"%(tempobject.display_name(request)), 'instance': tempclass})


def nested(request, classname, classname_dependent, id=None):
  messages = []
  Class = get_class("%s"%classname)
  tempobject = Class()
  ClassForm = get_class("%sForm"%classname)
  ClassDependent = get_class("%s"%classname_dependent)
  ClassDependentFormSet = inlineformset_factory(Class, ClassDependent, exclude=())
  if id==None:
    tempclass = Class()
  else:
    tempclass = Class.objects.get(pk=id)

  if request.method == 'POST':
    print("nested function post")
    formset = ClassDependentFormSet(request.POST, instance = tempclass)
    form = ClassForm(request, request.POST, instance = tempclass)
#    if formset.is_valid() and form.is_valid():
#      form.save()
#      formset.save()
#      return None, None
  else:
    message = request.GET.get('message', '')
    if message:
      messages = [message,]
    form = ClassForm(request, instance=tempclass)
    formset = ClassDependentFormSet(instance=tempclass)

  return form, formset
#  return render_to_response(tempobject.template(request), {'title': tempobject.display_name(request), 'header': tempobject.display_name(request), 'form':form, 'formset': formset, 'form_set':ClassDependent.form_set(), 'messages': messages, 'create_url':tempobject.create_url(request)})


