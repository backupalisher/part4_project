from django.db import connections
from django.shortcuts import render
import db_model.models as models


# Create your views here.


def _query(q):
    data = None
    with connections['part4'].cursor() as c:
        try:
            c.execute("BEGIN")
            c.execute(q)
            data = c.fetchall()
            c.execute("COMMIT")
        finally:
            c.close()
            return data


def index(request):
    title = 'Каритриджи'
    brands = models.Brands.objects.all()
    return render(request, 'cartridge/index.html', {'title': title, 'brands': brands})


def cartridges(request, brand_id):
    title = 'Каритриджи'
    cartridges = _query(f"SELECT * FROM all_cartridge WHERE brand_id = {brand_id} ORDER BY id")
    for idx in range(len(cartridges)):
        cartridge = list(cartridges[idx])
        cartridge[4] = list(set(cartridge[4]))
        cartridges[idx] = tuple(cartridge)
        cartridge_alt = list(cartridges[idx])
        cartridge_alt[8] = list(set(cartridge[8]))
        cartridges[idx] = tuple(cartridge_alt)
        brand = cartridge[7]

    # print([list(v) for v in dict(cartridge[7]).items()])

    return render(request, 'cartridge/cartridges.html', {'title': title, 'cartridges': cartridges, 'brand': brand})


def cartridge(request, cartridge_id):
    title = 'Каритридж'
    options = _query(f"SELECT * FROM all_options_for_cartridges WHERE id = {cartridge_id}")
    cartridge = _query(f"SELECT * FROM all_cartridge WHERE id = {cartridge_id}")[0]
    carts = list(cartridge)
    ids = list(set(carts[5]))
    models = list(set(carts[4]))
    brand_id = carts[6]
    brand = carts[7]
    arr = []
    for idx, v in enumerate(models):
        arr.append([ids[idx], v])
    carts[4] = arr
    cartridge = tuple(carts)
    return render(request, 'cartridge/cartridge.html', {'title': title, 'cartridge': cartridge, 'options': options,
                                                        'brand': brand, 'brand_id': brand_id})
