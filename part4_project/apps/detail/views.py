import asyncio
import concurrent.futures
import datetime

from asgiref.sync import sync_to_async
from django.http import Http404
from django.shortcuts import render

import db_model.models as models
from db_model.db_utils import _query

start_time = datetime.datetime.now()


def detail_view(request):
    return render(request, 'partcode/index.html')


# добавление веса
@sync_to_async
def set_weight(partcode_id):
    _query(
        f"UPDATE details SET weight = (w.weight+1) FROM (SELECT weight FROM details WHERE partcode_id = {partcode_id}) w "
        f"WHERE partcode_id = {partcode_id}")


@sync_to_async
def get_partcode(partcode_id):
    return _query(f"SELECT * FROM full_partcodes WHERE id =  {partcode_id}")


@sync_to_async
def get_options(detail_id):
    q_options = f"SELECT * FROM all_options_for_details WHERE detail_id = {detail_id}"
    option_vals = _query(q_options)
    captions = []
    subcaptions = []
    values = []
    for opts in option_vals:
        if opts[0] is None and opts[1] is None:
            for i in range(len(opts[3])):
                opts[3][i] = opts[3][i].replace('Caption: ', '')
            captions.append(opts)
        if opts[0] is None and opts[1] is not None:
            for opt in opts[3]:
                if 'SubCaption' in opt:
                    opts[3].remove(opt)
            subcaptions.append(opts)
        else:
            values.append(opts)
    options = option_vals
    return options, captions, subcaptions, values


@sync_to_async
def get_cartridge_options(partcode):
    cartridge_options = _query(f"SELECT * FROM all_options_for_cartridges WHERE code = '{partcode}'")
    return cartridge_options


async def init(partcode_id):
    async_tasks = [get_partcode(partcode_id)]
    # async_tasks = [get_options(partcode_id), get_partcode(partcode_id)]
    results = await asyncio.gather(*async_tasks)
    return results


async def past_init(request, partcode):
    if partcode != '-':
        tasks = [get_cartridge_options(partcode),]
        results = await asyncio.gather(*tasks)
        return results
    else:
        return []


def index(request, partcode_id):
    lang = request.LANGUAGE_CODE
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    loop.create_task(set_weight(partcode_id))
    try:
        init_result = list(loop.run_until_complete(init(partcode_id))[0][0])
    except:
        init_result = None
    vendors = models.Vendors.objects.all()
    try:
        model_ids = init_result[1]
        model_names = init_result[2]
        module_ids = init_result[3]
        module_names = init_result[4]
        module_ru_names = init_result[5]
        detail_name = init_result[7]
        detail_name_ru = init_result[8]
        description = init_result[9]
        partcode_description = init_result[10]
        partcode = init_result[11]
        images = init_result[12]
        prices = list(set(init_result[13]))
        vendor_ids = list(set(init_result[14]))
        options = None
        captions = None
        subcaptions = None
        values = None
        try:
            cartridge_options = loop.run_until_complete(get_cartridge_options(partcode))
        except:
            cartridge_options = None
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        v_prices = []
        c_models = []
        for i in range(len(prices)):
            v_prices.append([prices[i], vendor_ids[i]])
        for i in range(len(module_ids)):
            c_models.append([model_ids[i], model_names[i], module_ids[i], module_names[i], module_ru_names[i]])
    except:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        raise Http404('Страница отсутствует, с id: ' + str(partcode_id))
    return render(request, 'partcode/index.html',
                  {'lang': lang, "vendors": str(list(vendors.values_list())), 'cartridge_options': cartridge_options,
                   'c_models': c_models, 'v_prices': v_prices,
                   'detail_name': detail_name, 'detail_name_ru': detail_name_ru, 'options': options,
                   'description': description, 'partcode_description': partcode_description, 'images': images,
                   'captions': captions, 'subcaptions': subcaptions, 'values': values, 'partcode': partcode})
