import asyncio
import concurrent.futures
import datetime

from asgiref.sync import sync_to_async
from django.db import connections
from django.shortcuts import render

import db_model.models as models

start_time = datetime.datetime.now()


def index(request):
    brands = models.Brands.objects.all()
    return render(request, 'main/index.html', context={'search_block': True, 'brands': brands})


@sync_to_async
def search_detail(sval):
    with connections['part4'].cursor() as c:
        try:
            c.execute("BEGIN")
            c.callproc('details_search_v1', (sval,))
            ar = c.fetchall()
            c.execute("COMMIT")
        finally:
            c.close()
        return ar


@sync_to_async
def search_error(sval):
    with connections['part4'].cursor() as c:
        try:
            c.execute("BEGIN")
            c.callproc('error_search', (sval,))
            er = c.fetchall()
            c.execute("COMMIT")
        finally:
            c.close()
        return er


@sync_to_async
def search_cartridge(sval):
    with connections['part4'].cursor() as c:
        try:
            c.execute("BEGIN")
            c.callproc('cartridge_search', (sval,))
            cr = c.fetchall()
            c.execute("COMMIT")
        finally:
            c.close()
        return cr


async def init(sval):
    async_tasks = [search_detail(sval), search_error(sval), search_cartridge(sval)]
    results = await asyncio.gather(*async_tasks)
    return results


def search(request):
    variant = 0
    s_value = ''
    for item in request.GET:
        if 's' in item:
            s_value = request.GET.__getitem__('s')
        if 'v' in item:
            variant = int(request.GET.__getitem__('v'))
    ar = None
    er = None
    cr = None
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    result = loop.run_until_complete(init(s_value))
    ar = result[0]
    er = result[1]
    cr = result[2]
    return render(request, 'main/index.html',
                  context={'all_result': ar, 'error_result': er, 'cartridge_result': cr})
