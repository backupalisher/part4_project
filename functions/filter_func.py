import asyncio
import concurrent.futures
import json

from asgiref.sync import sync_to_async

import db_model.models as models
from db_model.db_utils import _query


# Function for get option ids from range and generate sql parts
def sql_get_range(cid, rmin, rmax):
    if rmin:
        pass
    else:
        rmin = 0
    if rmax:
        pass
    else:
        rmax = 1000000
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
            f'SELECT * FROM model_for_filter WHERE price is not null LIMIT {limit} OFFSET {offset} ORDER BY weight DESC, main_image;')
    elif target == 'supplies':
        brand_models = _query(
            f'SELECT * FROM all_partcodes WHERE supplies is null LIMIT {limit} OFFSET {offset};')
    else:
        brand_models = _query(
            f'SELECT * FROM model_for_filter ORDER BY weight DESC, main_image LIMIT {limit} OFFSET {offset};')
    # print(datetime.datetime.now() - start_time, 'получение всех моделей завершено')
    return brand_models


def get_supplies(partcode_id):
    return _query(f"""SELECT * FROM all_supplies WHERE id = {partcode_id};""")


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
            description_en, description_ru, brand_id, brand, models 
            FROM all_partcodes WHERE supplies is not null and brand_id in ({brand_id}) ORDER BY weight DESC, images;""")
        else:
            return _query(f"""SELECT id, code, article_code, images, description, name_en, name_ru, image, 
            description_en, description_ru, brand_id, brand, models 
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

# async def fpreload(brands, checkboxs, ranges, radios):
#     tasks = [get_filtered_model(brands, checkboxs, ranges, radios)]
#     results = await asyncio.gather(*tasks)
#     return results