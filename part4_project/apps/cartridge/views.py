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
    # print(cartridges)
    for idx in range(len(cartridges)):
        # print(cartridges)
        cartridge = list(cartridges[idx])
        cartridge[4] = list(set(cartridge[4]))
        cartridges[idx] = tuple(cartridge)
        cartridge_alt = list(cartridges[idx])
        cartridge_alt[8] = list(set(cartridge[8]))
        cartridges[idx] = tuple(cartridge_alt)

    # print([list(v) for v in dict(cartridge[7]).items()])

    return render(request, 'cartridge/cartridges.html', {'title': title, 'cartridges': cartridges})


def cartridge(request, cartridge_id):
    title = 'Каритридж'
    options = _query(
        f"SELECT sco.text FROM (SELECT ca.id FROM cartridge ca "
        f"LEFT JOIN partcodes pc ON pc.code = ca.code WHERE ca.id = {cartridge_id}) cart, link_cartridge_options lco "
        f"LEFT JOIN spr_cartridge_options sco ON lco.spr_cartridge_id = sco.id WHERE lco.cartridge_id = cart.id")
    cartridge = _query(
        f"SELECT cart.id, cart.code, cart.name, cart.name_ru, array_agg(m.name) AS model, array_agg(m.id) as model_id, "
        f"array_agg(cam.model) AS alt_model FROM cartridge cart "
        f"LEFT JOIN link_model_cartridge lmc ON lmc.cartridge_id = cart.id "
        f"LEFT JOIN models m ON m.id = lmc.model_id "
        f"LEFT JOIN link_cartridge_model_analog lcma ON lcma.cartridge_id = cart.id "
        f"LEFT JOIN cartridge_analog_model cam ON cam.id = lcma.cartrindge_analog_model_id "
        f"WHERE cart.id = {cartridge_id} GROUP BY cart.id, cart.code, cart.name, cart.name_ru")
    carts = list(cartridge[0])
    ids = list(set(carts[5]))
    models = list(set(carts[4]))
    arr = []
    for idx, v in enumerate(models):
        arr.append([ids[idx], v])
    print(arr)
    carts[4] = arr
    # carts[5] =
    carts[6] = list(set(carts[6]))
    cartridge[0] = tuple(carts)
    return render(request, 'cartridge/cartridge.html', {'title': title, 'cartridge': cartridge[0], 'options': options})
