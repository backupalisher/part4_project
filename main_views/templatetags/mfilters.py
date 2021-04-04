from django import template

register = template.Library()


@register.filter
def get_caption(obj):
    return obj.split(':')[0]


@register.filter
def get_val(obj):
    return obj.split(':')[1]


@register.filter
def list_item(lst, i):
    try:
        return lst[i]
    except:
        return None


@register.filter
def divide(value, arg):
    return str(round(float(value)/arg, 2))