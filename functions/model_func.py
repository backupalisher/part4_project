import asyncio

from asgiref.sync import sync_to_async

from db_model.db_utils import _query


# добавление веса
@sync_to_async
def set_weight(model_id):
    _query(f"""UPDATE models SET weight = (w.weight+1) FROM (SELECT weight FROM models WHERE id = {model_id}) w 
            WHERE id = {model_id}""")


# Запрос на получение опций и вывод опций
@sync_to_async
def get_options(request, model_id):
    lang = request.LANGUAGE_CODE
    if lang == 'ru':
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
            # 'Снят с производства',
            # 'Актуальный',
        ]
    else:
        captions = [
            'Common options',
            'Printer',
            'Copier',
            'Scanner',
            'Consumables',
            'Fax',
            'Telephone',
            'Fonts and control languages',
            'Feeder',
            'Finisher',
            'Interface',
            'Memory/Processor',
            'Additional information',
            'Photo',
            'General information',
            'Size',
            # 'Снят с производства',
            # 'Актуальный',
        ]
    options = []
    option_vals = _query(f"SELECT * FROM all_options_by_model WHERE id = {model_id};")
    print(option_vals)
    if option_vals:
        if lang == 'ru':
            for opt in option_vals[0][2]:
                opts = opt.split('~')
                capt = opts[0].split(';')
                caption = capt[0].strip()
                subcaption = capt[1].strip()
                val = opts[1].strip()
                options.append([caption, subcaption, val])
        else:
            for opt in option_vals[0][3]:
                opts = opt.split('~')
                capt = opts[0].split(';')
                caption = capt[0].strip()
                subcaption = capt[1].strip()
                val = opts[1].strip()
                options.append([caption, subcaption, val])
            # if opts[0] is None and opts[1] is not None:
            #     for opt in opts[3]:
            #         if 'SubCaption' in opt:
            #             opts[3].remove(opt)
            #     subcaptions.append(opts)
            # else:
            #     values.append(opts)
    return options, captions


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
    partcatalog = _query(f'SELECT * FROM partcodes_by_model WHERE id = {model_id} ORDER BY module_en;')

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
    # supplies = _query(f"SELECT * FROM partcodes_by_model WHERE id = {model_id} and supplies is true")
    supplies = _query(f"""SELECT ap.* FROM models m LEFT JOIN link_model_supplies lms ON lms.model_id = m.id
                    LEFT JOIN all_partcodes ap ON ap.id = lms.supplies_id WHERE m.id = {model_id}""")
    # for idx in range(len(supplies)):
    #     supp = list(supplies[idx])
    #     supp[4] = list(set(supp[4]))
    #     supplies[idx] = tuple(supp)
    #     supp_alt = list(supplies[idx])
    #     supp_alt[8] = list(set(supp[8]))
    #     supplies[idx] = tuple(supp_alt)
    return supplies


async def init(request, model_id):
    tasks = [
        get_model(model_id),
        get_options(request, model_id),
        qet_partcatalog(request, model_id),
        get_errors(model_id),
        get_supplies(model_id),
        set_weight(model_id)
    ]
    results = await asyncio.gather(*tasks)
    return results
