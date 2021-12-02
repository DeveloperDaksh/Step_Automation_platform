from django.template.defaulttags import register


@register.filter
def splicestring(filestring, userlength):
    return filestring.name[userlength:]
