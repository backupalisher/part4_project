import asyncio
import concurrent.futures
import datetime

from asgiref.sync import sync_to_async
from django.http import Http404
from django.shortcuts import render

from db_model.db_utils import _query

start_time = datetime.datetime.now()


def detail_view(request):
    return render(request, '/models/index.html')


# добавление веса
@sync_to_async
def set_weight(model_id):
    _query(f"""UPDATE models SET weight = (w.weight+1) FROM (SELECT weight FROM models WHERE id = {model_id}) w 
            WHERE id = {model_id}""")


# Запрос на получение опций и вывод опций
@sync_to_async
def get_options(detail_id):
    captions = [
        'Общие характеристики',
        'Принтер',
        'Копир',
        'Сканер',
        'Расходные материалы',
        'Факс',
        'Телефон',
        'Шрифты и языки управления',
        'Лотки',
        'Финишер',
        'Интерфейсы',
        'Память/Процессор',
        'Дополнительная информация',
        'Фото',
        'Общая информация',
        'Габариты',
        'Снят с производства',
        'Актуальный',
    ]
    subcaptions = []
    values = []
    option_vals = _query(f"SELECT * FROM all_options_model WHERE detail_id = {detail_id};")

    for opts in option_vals:
        if opts[0] is None and opts[1] is not None:
            for opt in opts[3]:
                if 'SubCaption' in opt:
                    opts[3].remove(opt)
            subcaptions.append(opts)
        else:
            values.append(opts)
    options = option_vals
    return options, captions, subcaptions, values


# Запрос на получение ошибок
@sync_to_async
def get_errors(model_id):
    verrors = _query(f"SELECT * FROM all_errors WHERE mid = {model_id}  ORDER BY code;")

    if len(verrors) > 0:
        if verrors[0][2] is None and verrors[0][3] is None and verrors[0][4] is None and verrors[0][5] is None:
            verrors = None
    return verrors


# Запрос на получение парткодов и модулей
@sync_to_async
def qet_partcatalog(request, model_id):
    # 'Получение id парткодов, моделей, модулей, названий детали для модулей и парткаталога', q_code_module)
    modules = []
    partcatalog = _query(f'SELECT * FROM partcatalog WHERE model_id = {model_id} and supplies is not true;')

    if partcatalog and len(partcatalog) > 0:
        for parts in partcatalog:
            modules.append([parts[3], parts[4]])
    b_set = set(tuple(x) for x in modules)
    modules = [list(x) for x in b_set]
    if request.GET.get('module'):
        cur_module = request.GET.get('module')
    else:
        cur_module = None

    return modules, cur_module, partcatalog


# Получение данных для модели
@sync_to_async
def get_model(model_id):
    return _query(f'SELECT * FROM model_for_filter WHERE mid = {model_id}')


# Получение данных картриджей
@sync_to_async
def get_supplies(model_id):
    supplies = _query(f"SELECT * FROM partcatalog WHERE model_id = {model_id} and supplies is true")
    for idx in range(len(supplies)):
        supp = list(supplies[idx])
        supp[4] = list(set(supp[4]))
        supplies[idx] = tuple(supp)
        supp_alt = list(supplies[idx])
        supp_alt[8] = list(set(supp[8]))
        supplies[idx] = tuple(supp_alt)
    return supplies


async def init(model_id):
    async_tasks = [get_model(model_id)]
    results = await asyncio.gather(*async_tasks)
    return results


async def past_init(request, model_id):
    tasks = [
        qet_partcatalog(request, model_id),
        get_errors(model_id),
        get_supplies(model_id)
    ]
    results = await asyncio.gather(*tasks)
    return results


def index(request, model_id):
    lang = request.LANGUAGE_CODE
    tabs = [
        'options',
        'parts',
        'errors',
        'supplies'
    ]
    tab = request.GET.get('tab')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    init_result = loop.run_until_complete(init(model_id))[0][0]
    model_id = init_result[0]
    model_name = init_result[1]
    model_main_image = init_result[3]
    model_images = init_result[4]
    brand_id = init_result[5]
    brand_name = init_result[6]
    options_ru = []
    model_status = ''
    for opt in init_result[10]:
        if opt:
            optL = opt.split(':')
            options_ru.append(optL)
            if optL[0] == 'Status':
                model_status = optL[1]
    options_en = []
    for opt in init_result[11]:
        if opt:
            optL = opt.split(':')
            options_en.append(optL)
            if optL[0] == 'Status':
                model_status = optL[1]
    price = init_result[8]
    vendor = init_result[9]
    loop.create_task(set_weight(model_id))
    post_result = loop.run_until_complete(past_init(request, model_id))
    options = None
    captions = None
    subcaptions = None
    values = None
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
    modules = post_result[0][0]
    cur_module = post_result[0][1]
    partcatalog = post_result[0][2]
    verrors = post_result[1]
    supplies = post_result[2]
    if tab:
        pass
    elif cur_module is not None:
        tab = 'parts'
    else:
        tab = 'options'
        try:
            if len(supplies) > 0:
                tab = 'supplies'
        except:
            pass
        try:
            if len(verrors) > 0:
                tab = 'errors'
        except:
            pass
        try:
            if len(partcatalog) > 0:
                tab = 'parts'
        except:
            pass
        try:
            if len(subcaptions) > 0:
                tab = 'options'
        except:
            pass

    if model_id:
        return render(request, 'main/models.html',
                      {'model_name': model_name, 'model_main_image': model_main_image,
                       'modules': modules, 'verrors': verrors, 'model_images': model_images, 'options': options,
                       'partcatalog': partcatalog, 'captions': captions, 'brand_id': brand_id, 'brand_name': brand_name,
                       'subcaptions': subcaptions, 'values': values, 'cur_module': cur_module, 'supplies': supplies,
                       'tab': tab,  'lang': lang, 'model_status': model_status, 'price': price, 'vendor': vendor})
    else:
        raise Http404('Страница отсутствует, с id: ' + str(model_id))
