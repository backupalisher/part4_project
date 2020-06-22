from django.http import Http404
from django.shortcuts import render

import db_model.models as models
from db_model.db_utils import _query


# Create your views here.


def index(request):
    title = 'Каритриджи'
    brands = models.Brands.objects.all()
    return render(request, 'cartridge/index.html', {'title': title, 'brands': brands})


def cartridges(request, brand_id):
    title = 'Каритриджи'
    cartridges = _query(f"SELECT * FROM all_cartridge WHERE brand_id = {brand_id} ORDER BY id")
    brand = ''
    for idx in range(len(cartridges)):
        cartridge = list(cartridges[idx])
        cartridge[4] = list(set(cartridge[4]))
        cartridges[idx] = tuple(cartridge)
        cartridge_alt = list(cartridges[idx])
        cartridge_alt[8] = list(set(cartridge[8]))
        cartridges[idx] = tuple(cartridge_alt)
        if cartridge[7]:
            brand = cartridge[7]
        else:
            brand = ''

    return render(request, 'cartridge/cartridges.html', {'title': title, 'cartridges': cartridges, 'brand': brand})


def cartridge(request, cartridge_id):
    title = 'Каритридж'
    options = _query(f"SELECT * FROM all_options_for_cartridges WHERE id = {cartridge_id}")
    cartridge = _query(f"SELECT * FROM all_cartridge WHERE id = {cartridge_id}")
    if cartridge:
        carts = list(cartridge[0])
        tids = set()
        tmodels = set()
        tamodels = set()
        # ids = list(set(carts[5]))
        ids = [x for x in carts[5] if not (x in tids or tids.add(x))]
        # models = list(set(carts[4]))
        models = [x for x in carts[4] if not (x in tmodels or tmodels.add(x))]
        brand_id = carts[6]
        if carts[7]:
            brand = carts[7]
        else:
            brand = ''
        arr = []
        for idx, v in enumerate(models):
            arr.append([ids[idx], v])
        carts[4] = arr
        amodels = [x for x in carts[8] if not (x in tamodels or tamodels.add(x))]
        cartridge = tuple(carts)
        return render(request, 'cartridge/cartridge.html', {'title': title, 'cartridge': cartridge, 'options': options,
                                                            'brand': brand, 'brand_id': brand_id, 'amodels': amodels})
    else:
        raise Http404('Страница отсутствует, с id: ' + str(cartridge_id))
