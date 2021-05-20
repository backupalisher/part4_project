import asyncio
import concurrent.futures
import datetime
import json

from asgiref.sync import sync_to_async

import db_model.models as models
from db_model.db_utils import _query

# Function for get option ids from range and generate sql parts
from sendmail.services import send


def sql_get_range(cid, rmin, rmax):
    if rmin:
        pass
    else:
        rmin = 0
    if rmax:
        pass
    else:
        rmax = 2000000
    q = f'SELECT * FROM select_id_for_range({cid}, {rmin}, {rmax})'
    rids = _query(q)
    for i, rid in enumerate(rids):
        if i == 0:
            sq = f'( mopt.ids && ARRAY[{rid[0]}]'
        else:
            sq += f' OR mopt.ids && ARRAY[{rid[0]}]'
    sq += ')'
    return sq


def sql_gen_checks(checks):
    cq = ' mopt.ids && ARRAY['
    for i, check in enumerate(checks):
        if i == 0:
            cq += f'{check}'
        else:
            cq += f',{check}'
    cq += '] '
    return cq


def get_filters():
    # print(datetime.datetime.now() - start_time, 'получение фильтров')
    sfilter = models.FilterSettings.objects.all().order_by('id')
    # print(datetime.datetime.now() - start_time, 'получение фильтров завершено')
    return sfilter


# @sync_to_async
def get_all_models(limit, offset, target):
    # print(datetime.datetime.now() - start_time, 'получение всех моделей')
    if target == 'market':
        brand_models = _query(
            f"""SELECT * FROM model_for_filter WHERE prices::text not ilike '%NULL%' ORDER BY weight DESC, main_image 
            LIMIT {limit} OFFSET {offset};""")
    elif target == 'supplies':
        brand_models = _query(
            f'SELECT * FROM all_partcodes WHERE supplies is null LIMIT {limit} OFFSET {offset};')
    else:
        brand_models = _query(
            f'SELECT * FROM model_for_filter ORDER BY weight DESC, main_image LIMIT {limit} OFFSET {offset};')
    # print(datetime.datetime.now() - start_time, 'получение всех моделей завершено')
    return brand_models


def get_partcode(partcode_id):
    return _query(f"""SELECT * FROM all_partcodes WHERE id = {partcode_id};""")


def get_partcodes(target, model_id=None, brand_id=None):
    if model_id:
        return _query(f'SELECT * FROM all_partcodes ORDER BY weight DESC, images;')
    elif target == 'all':
        return _query(f'SELECT * FROM all_partcodes ORDER BY weight DESC, images;')
    elif target == 'supplies':
        if brand_id:
            return _query(f"""SELECT id, code, article_code, images, description, name_en, name_ru, image, 
            description_en, description_ru, brand_id, brand, analog_models 
            FROM all_partcodes WHERE supplies is not null and brand_id in ({brand_id}) ORDER BY weight DESC, images;""")
        else:
            return _query(f"""SELECT id, code, article_code, images, description, name_en, name_ru, image, 
            description_en, description_ru, brand_id, brand, analog_models 
            FROM all_partcodes WHERE supplies is not null ORDER BY weight DESC, images;""")
    else:
        return _query(f'SELECT * FROM all_partcodes ORDER BY weight DESC, images;')


# @sync_to_async
def get_filtered_model(brands, checkboxs, ranges, radios):
    checkboxs = json.loads(str(checkboxs))
    ranges = json.loads(str(ranges))
    radios = json.loads(str(radios))
    f_sql = f'SELECT * FROM model_for_filter mopt WHERE '
    ops = 0
    if len(checkboxs) > 0 or len(ranges) > 0 or len(radios) > 0:
        f_sql += f'('
        for key, value in ranges.items():
            if len(value) > 0:
                if ops == 0:
                    f_sql += sql_get_range(key.replace('range', ''), value[0], value[1])
                    ops += 1
                else:
                    f_sql += ' AND '
                    f_sql += sql_get_range(key.replace('range', ''), value[0], value[1])
        for key, value in radios.items():
            if len(value) > 0:
                if ops == 0:
                    f_sql += (f'mopt.ids && ARRAY[{value}]')
                    ops += 1
                else:
                    f_sql += ' AND '
                    f_sql += (f'mopt.ids && ARRAY[{value}]')
        for key, value in checkboxs.items():
            if len(value) > 0:
                if ops == 0:
                    f_sql += sql_gen_checks(value)
                    ops += 1
                else:
                    f_sql += ' AND '
                    f_sql += sql_gen_checks(value)
        f_sql += f' ) '
        if len(brands) > 0:
            f_sql += f' AND'
    if len(brands) > 0:
        f_sql += f' ('
        for i, bid in enumerate(brands):
            if i + 1 != len(brands):
                f_sql += f'brand_id = {int(bid)} OR '
            else:
                f_sql += f'brand_id = {int(bid)} )'
    f_sql += f' ORDER BY weight DESC, main_image;'
    brand_models = _query(f_sql)
    return brand_models


def add_cart_item(price_id, user_id, date, count):
    q = f"""UPDATE cart SET count = cart.count + 1 WHERE price_id = {price_id} and user_id = {user_id};
            INSERT INTO cart (price_id, user_id, date, status, count) 
            SELECT {price_id}, {user_id}, '{date}', true, {count}
            WHERE NOT EXISTS (SELECT 1 FROM cart WHERE price_id = {price_id} and user_id = {user_id});"""
    _query(q)
    return True


def remove_cart_item(price_id, user_id):
    q = f"""DELETE FROM cart WHERE price_id = {price_id} AND user_id = {user_id}"""
    _query(q)
    return True


def change_cart_count(price_id, user_id, value):
    q = ''
    if value == 'plus':
        q = f"""UPDATE cart SET count = cart.count + 1 WHERE price_id = {price_id} and user_id = {user_id};"""
    elif value == 'minus':
        q = f"""UPDATE cart SET count = cart.count - 1 WHERE price_id = {price_id} and user_id = {user_id};"""
    _query(q)
    return True


def select_cart_items(user_id, active):
    q = f"""SELECT cart.cart_id, cart.date, concat(ap.code, ' ', ap.name_en, ' ', ap.name_ru, ' ', am.model_name) 
            orders, cart.count, p.price, p.partcode_id, p.model_id, cart.price_id, p.count as counts, p.vendor_id 
            FROM cart  LEFT JOIN prices p ON p.id = price_id
            LEFT JOIN vendors v ON v.id = p.vendor_id
            LEFT JOIN all_partcodes ap ON ap.id = p.partcode_id
            LEFT JOIN all_models am ON am.model_id = p.model_id
            WHERE user_id = {user_id} AND status = {active};"""
    return _query(q)


def get_orders(request):
    orders = []
    cart_history = _query(f"""SELECT cart.cart_id, cart.date, concat(ap.code, ' ', ap.name_en, ' ', ap.name_ru, ' ', am.model_name) 
            orders, cart.count, cart.price, cart.status, cart.partcode_id, cart.model_id FROM cart_history cart
            LEFT JOIN vendors v ON v.id = cart.vendors_id
            LEFT JOIN all_partcodes ap ON ap.id = cart.partcode_id
            LEFT JOIN all_models am ON am.model_id = cart.model_id
            WHERE user_id = {request.user.id};""")
    ors = _query(f'SELECT * FROM orders WHERE orders.user_id = {request.user.id};')
    for order in ors:
        hists = []
        total = 0
        for hist in cart_history:
            if hist[0] in order[4]:
                total += total + float(hist[4])
                hists.append({
                    'date': hist[1],
                    'orders': hist[2],
                    'count': hist[3],
                    'price': hist[4],
                    'status': hist[5],
                    'partcode_id': hist[6],
                    'model_id': hist[7]
                })
        if len(hists) > 0:
            o_item = {'order_num': order[0], 'address': order[2], 'phone': order[3], 'status': order[5],
                      'cart_history': hists, 'total': total}
            orders.append(o_item)
    return orders


def order_cart(request):
    if 'cart_items' in request.POST:
        items = []
        for item in json.loads(request.POST['cart_items']):
            items.append(item['cart_id'])
            model_id = 'null'
            partcode_id = 'null'
            if item['model_id']:
                model_id = item['model_id']
            if item['partcode_id']:
                partcode_id = item['partcode_id']
            _query(f"""INSERT INTO cart_history(cart_id, date, status, count, user_id, price, model_id, partcode_id, 
            vendors_id) VALUES ({item['cart_id']}, '{datetime.datetime.now()}', 'new', {item['count']}, 
            {request.user.id}, {item['price']}, {model_id}, {partcode_id}, {item['vendor_id']})""")
        order_q = f"""INSERT INTO orders(user_id, address, phone, cart_id, status) VALUES ({request.user.id}, 
        '{request.POST['address']}', '{request.POST['phone']}', '{items}', 'new') RETURNING ID"""
        order = _query(order_q)[0][0]
        print(order)
        # send(request, order)
        return order

# async def fpreload(brands, checkboxs, ranges, radios):
#     tasks = [get_filtered_model(brands, checkboxs, ranges, radios)]
#     results = await asyncio.gather(*tasks)
#     return results
