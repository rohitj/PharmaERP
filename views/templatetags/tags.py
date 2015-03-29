from django import template

register = template.Library()

def Convert(type, value=None):
  if type=="edit":
    return "<img src='/site_media/images/b_edit.png' alt='edit' title='edit' />"
  elif type=="view":
    return "<img src='/site_media/images/b_view.png' alt='view' title='view' />"
  elif type=="add_dependent":
    alt = "add dependent"
    if value:
      alt = value
    return "<img src='/site_media/images/add_dependent.png' alt='" + alt + "' title='" + alt + "' />"
  elif type=="delete":
    return "<img src='/site_media/images/b_drop.png' alt='delete' title='delete' />"
  elif type=="access":
    return "<img src='/site_media/images/s_rights.png' alt='change access rights' title='change access rights' />"
  elif type=="passwd":
    return "<img src='/site_media/images/s_passwd.png' alt='change passwd' title='change passwd' />"
  elif type=="reply":
    return "<img src='/site_media/images/reply.png' width='20' alt='reply' title='reply' />"
  elif type=="replyall":
    return "<img src='/site_media/images/replyall.png' width='20' alt='reply all' title='reply all' />"
  return "<img src='/site_media/images/b_delete.png' alt='delete' />"

#@register.filter
#def convert_to_img(value, type):
#  edit = "<img href='/site_media/images/b_edit.png' alt='edit' />"
#  view = "<img href='/site_media/images/b_view.png' alt='view' />"
#  delete = "<img href='/site_media/images/b_delete.png' alt='delete' />"
#  if type=="edit":
#    return edit
#  elif type=="view":
#    return view
#  elif type=="delete":
#    return delete
#  return delete


@register.simple_tag
def convert_to_img(type, value=None):
  return Convert(type, value)
#convert_to img = register.tag(convert_to_img)

@register.simple_tag
def args(vars, var, value):
  vars = vars.copy()
  vars[var] = value
  return vars.urlencode()


def callMethod(obj, methodName):
  method = getattr(obj, methodName)
 
  if obj.__dict__.has_key("__callArg"):
    ret = method(*obj.__callArg)
    del obj.__callArg
    return ret
  return method()
 
def args(obj, arg):
  if not obj.__dict__.has_key("__callArg"):
    obj.__callArg = []

  obj.__callArg += [arg]
  return obj

register.filter("call", callMethod)
register.filter("args", args)
