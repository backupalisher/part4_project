import asyncio
import concurrent.futures

from django.http import Http404

from functions.model_func import init


def model_index(request, model_id):
    lang = request.LANGUAGE_CODE
    tab = request.GET.get('tab')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=4))
    init_result = loop.run_until_complete(init(request, model_id))
    model, all_options, partcatalog, errors, supplies, weight = init_result
    model = model[0]
    model_name = model[1]
    model_main_image = model[3]
    model_images = model[4]
    brand_id = model[5]
    brand_name = model[6]
    options_m = []
    model_status = ''
    if model[10]:
        for opt in model[10]:
            if opt:
                optL = opt.split(':')
                options_m.append(optL)
                if optL[0] == 'Status':
                    model_status = optL[1]
    price = model[8]
    vendor = model[9]
    if partcatalog:
        modules = partcatalog[0]
        cur_module = partcatalog[1]
        partcatalog = partcatalog[2]
    else:
        modules = []
        cur_module = None
        partcatalog = []
    if errors:
        verrors = errors
    else:
        verrors = []
    if supplies:
        supplies = supplies[0]
    else:
        supplies = []
    if all_options:
        scaptions = []
        captions = []
        options, tcatp = all_options
        for cap in tcatp:
            for opt in options:
                if opt[0] == cap:
                    scaptions.append(cap)
        scaptions = set(scaptions)
        for tcap in tcatp:
            for cap in scaptions:
                if tcap == cap:
                    captions.append(tcap)
        
    else:
        options = []
        captions = []
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
            if len(options) > 0:
                tab = 'options'
        except:
            pass

    if model_id:
        return 'models/item.html', {'model_name': model_name, 'model_main_image': model_main_image, 'modules': modules,
                                    'options_m': options_m, 'brand_name': brand_name,
                                    'verrors': verrors, 'model_images': model_images, 'options': options,
                                    'partcatalog': partcatalog, 'captions': captions, 'brand_id': brand_id,
                                    'cur_module': cur_module, 'supplies': supplies, 'tab': tab, 'lang': lang,
                                    'model_status': model_status, 'price': price, 'vendor': vendor}
    else:
        raise Http404('Страница отсутствует, с id: ' + str(model_id))
