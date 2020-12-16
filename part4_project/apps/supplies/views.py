from django.http import Http404, JsonResponse
from django.shortcuts import render

import db_model.models as models
from db_model.db_utils import _query


# Create your views here.

def supplie_sort(supplies):
    for idx in range(len(supplies)):
        supplie = list(supplies[idx])
        supplie[4] = list(set(supplie[4]))
        supplies[idx] = tuple(supplie)
        supplie_alt = list(supplies[idx])
        supplie_alt[8] = list(set(supplie[8]))
        supplies[idx] = tuple(supplie_alt)
        if supplie[7]:
            brand = supplie[7]
        else:
            brand = ''


def supplie_get(brand_id):
    f_sql = f"SELECT * FROM all_cartridge "
    if brand_id > 0:
        f_sql += f' WHERE brand_id = {brand_id}'
    f_sql += f" ORDER BY weight DESC, id;"
    print(f_sql)
    return _query(f_sql)


def index(request):
    lang = request.LANGUAGE_CODE
    title = 'Расходные материалы'
    brands = models.Brands.objects.all()
    try:
        brand = dict(request.GET.lists())['brand'][0]
        supplies = supplie_get(int(brand))
        return render(request, 'supplies/index.html', {'title': title, 'brands': brands, 'supplies': supplies})
    except:
        supplies = _query(f"SELECT * FROM all_cartridge ORDER BY weight DESC, id LIMIT 200;")
        return render(request, 'supplies/index.html',
                      {'title': title, 'brands': brands, 'supplies': supplies, 'lang': lang})


def supplies(request, brand_id):
    lang = request.LANGUAGE_CODE
    title = 'Расходные материалы'
    supplies = _query(f"SELECT * FROM all_cartridge WHERE brand_id = {brand_id} ORDER BY weight DESC, id")
    brand = ''

    return render(request, 'supplies/supplies.html',
                  {'title': title, 'supplies': supplies, 'brand': brand, 'lang': lang})


def supplie(request, supplie_id):
    _query(f"UPDATE cartridge SET weight = (w.weight+1) FROM (SELECT weight FROM cartridge WHERE id = {supplie_id}) "
           f"w WHERE id = {supplie_id}")
    lang = request.LANGUAGE_CODE
    title = 'Расходные материалы'
    options = _query(f"SELECT * FROM all_options_for_cartridges WHERE id = {supplie_id}")
    prices = _query(f"SELECT v.name, cartridge_price.price FROM cartridge_price "
                    f"LEFT JOIN vendors v ON v.id = cartridge_price.vendor_id WHERE cartridge_id = {supplie_id}")
    supplie = _query(f"SELECT * FROM all_cartridge WHERE id = {supplie_id}")
    if supplie:
        carts = list(supplie[0])
        tids = set()
        tmodels = set()
        tamodels = set()
        # ids = list(set(carts[5]))
        ids = [x for x in carts[5] if not (x in tids or tids.add(x))]
        # models = list(set(carts[4]))
        models = [x for x in carts[4] if not (x in tmodels or tmodels.add(x))]
        brand_id = carts[6]
        price = carts[10]
        vendor = carts[11]
        if carts[7]:
            brand = carts[7]
        else:
            brand = ''
        arr = []
        for idx, v in enumerate(models):
            arr.append([ids[idx], v])
        carts[4] = arr
        amodels = [x for x in carts[8] if not (x in tamodels or tamodels.add(x))]
        supplie = tuple(carts)
        return render(request, 'supplies/supplie.html', {'title': title, 'supplie': supplie, 'options': options,
                                                            'brand': brand, 'brand_id': brand_id, 'amodels': amodels,
                                                            'prices': prices, 'supplie_id': supplie_id, 'price': price,
                                                            'vendor': vendor, 'lang': lang})
    else:
        raise Http404('Страница отсутствует, с id: ' + str(supplie_id))
