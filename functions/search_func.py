import asyncio
import re

from asgiref.sync import sync_to_async
from django.db import connections

from db_model.db_utils import _query


# search in details
@sync_to_async
def search_detail(sval):
    aval = sval.replace(':', '').split(' ')
    sval = ''
    for val in aval:
        sval += val + ':* & '
    sval = re.sub(r'\s[&]\s$', '', sval)
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


# search in models
@sync_to_async
def search_models(sval):
    aval = sval.replace(':', '').split(' ')
    sval = '%'
    for val in aval:
        sval += val + '%'
    return _query(f"SELECT * FROM all_models WHERE trigrams ilike '{sval}'")


# init search
async def search_init(sval):
    async_tasks = [search_detail(sval), search_error(sval), search_cartridge(sval), search_models(sval)]
    results = await asyncio.gather(*async_tasks)
    return results


