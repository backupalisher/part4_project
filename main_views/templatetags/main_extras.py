from django import template
import locale

register = template.Library()
locale.setlocale(locale.LC_ALL, 'ru_RU')


@register.filter(name='d_mask')
def cut(value):
    try:
        mask = (locale.currency(int(value), False, grouping=True)).replace(',00', '')
        return mask
    except:
        return value
