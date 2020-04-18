from django import template


register = template.Library()
@register.filter
def minus(value, arg):
    return value - arg

@register.filter
def plus(value, arg):
    return value + arg

@register.filter
def mimage(value):
    images = value.split(';')
    if len(images) > 0:
        if images[0] != '':
            return images[0]
    else:
        return 'no-image.png'