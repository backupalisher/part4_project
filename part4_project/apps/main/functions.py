import asyncio
import json
import math

from asgiref.sync import sync_to_async
from django.db import connections
import db_model.models as models
from db_model.db_utils import _query


# search in details
@sync_to_async
def search_detail(sval):
    with connections['default'].cursor() as c:
        try:
            c.execute("BEGIN")
            c.callproc('details_search_v1', (sval,))
            ar = c.fetchall()
            c.execute("COMMIT")
        finally:
            c.close()
        return ar


# search in errors
@sync_to_async
def search_error(sval):
    with connections['default'].cursor() as c:
        try:
            c.execute("BEGIN")
            c.callproc('error_search', (sval,))
            er = c.fetchall()
            c.execute("COMMIT")
        finally:
            c.close()
        return er


# search in cartridges
@sync_to_async
def search_cartridge(sval):
    with connections['default'].cursor() as c:
        try:
            c.execute("BEGIN")
            c.callproc('cartridge_search', (sval,))
            cr = c.fetchall()
            c.execute("COMMIT")
        finally:
            c.close()
        return cr


# init search
async def search_init(sval):
    async_tasks = [search_detail(sval), search_error(sval), search_cartridge(sval)]
    results = await asyncio.gather(*async_tasks)
    return results


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
    sq = ''
    for i, rid in enumerate(rids):
        if i == 0:
            sq = f' mopt.ids && ARRAY[{rid[0]}]'
        else:
            sq += f' OR mopt.ids && ARRAY[{rid[0]}]'
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


@sync_to_async
def get_filters():
    # print(datetime.datetime.now() - start_time, 'получение фильтров')
    sfilter = models.FilterSettings.objects.all().order_by('id')
    # print(datetime.datetime.now() - start_time, 'получение фильтров завершено')
    return sfilter


@sync_to_async
def get_all_models(limit, offset):
    # print(datetime.datetime.now() - start_time, 'получение всех моделей')
    brand_models = _query(
        f'SELECT * FROM model_for_filter mopt ORDER BY weight DESC, main_image LIMIT {limit} OFFSET {offset};')
    # print(datetime.datetime.now() - start_time, 'получение всех моделей завершено')
    return brand_models


@sync_to_async
def get_filtered_model(brands, checkboxs, ranges, radios):
    checkboxs = json.loads(str(checkboxs))
    ranges = json.loads(str(ranges))
    radios = json.loads(str(radios))
    f_sql = f'SELECT * FROM model_for_filter mopt WHERE ('
    ops = 0
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
        f_sql += f'AND ('
        for i, bid in enumerate(brands):
            if i+1 != len(brands):
                f_sql += f'brand_id = {int(bid)} OR '
            else:
                f_sql += f'brand_id = {int(bid)} )'
    f_sql += f' ORDER BY main_image;'
    print(f_sql)
    brand_models = _query(f_sql)
    return brand_models


async def preload(limit, offset):
    tasks = [get_filters(), get_all_models(limit, offset)]
    results = await asyncio.gather(*tasks)
    return results


async def fpreload(brands, checkboxs, ranges, radios):
    tasks = [get_filtered_model(brands, checkboxs, ranges, radios)]
    results = await asyncio.gather(*tasks)
    return results
