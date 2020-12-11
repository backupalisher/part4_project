from django import template
import locale
import phonenumbers

register = template.Library()
locale.setlocale(locale.LC_ALL, 'ru_Ru')


@register.filter(name='d_mask')
def cut(value):
    try:
        mask = (locale.currency(int(value), False, grouping=True)).replace(',00', '')
        return mask
    except:
        return value


@register.filter(name='c_phone')
def fotmat(value):
    try:
        return phonenumbers.parse(value, "RU")
    except:
        return 'invalid'
