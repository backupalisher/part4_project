import json

import boto3
from django.http import JsonResponse
from django.shortcuts import render, redirect
from werkzeug.utils import secure_filename

from db_model.db_utils import _query
from db_model.models import *
from part4_project.env import *


# Create your views here.
def save_price(price, id, vendor, type, price_id):
    if price_id != 0:
        _query(f'UPDATE prices SET price = {price} WHERE id = {price_id};')
    else:
        if type == 'model':
            _query(f'INSERT INTO prices (price, model_id, vendor_id) VALUES ({price}, {id}, {vendor}) ;')
        if type == 'partcode':
            _query(f'INSERT INTO prices (price, partcode_id, vendor_id) VALUES ({price}, {id}, {vendor}) ;')
        if type == 'partcode':
            _query(f'INSERT INTO prices (price, detail_id, vendor_id) VALUES ({price}, {id}, {vendor}) ;')


def save_file(file_path, filename):
    # print(type(file_path), file_path)
    # print(type(filename), filename)
    # print(type(aws_bucket), aws_bucket)
    # print(type(aws_access_key_id), aws_access_key_id)
    # print(type(aws_secret_access_key), aws_secret_access_key)
    # conn = boto3.client(service_name='s3', endpoint_url='https://storage.yandexcloud.net',
    #                     aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    # with open(file_path, "rb") as f:
    #     conn.upload_fileobj(f, aws_bucket, filename)
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=aws_access_key_id[0],
        aws_secret_access_key=aws_secret_access_key
    )
    # with open(file_path, "rb") as f:
    s3.upload_file(file_path, aws_bucket, filename)
    # s3.Bucket(aws_bucket).put_object(Key=filename, Body=file)
    # print(secure_filename(file))
    # s3.put_object(Bucket=aws_bucket, Body=file, Key=secure_filename(filename), StorageClass='COLD')


def index(request):
    if not request.user.is_superuser:
        return redirect('/cabinet/')
    else:
        return render(request, 'dashboard/index.html', {'tab': 'index'})


def brands(request):
    if not request.user.is_superuser:
        return redirect('/cabinet/')
    else:
        if request.is_ajax():
            if request.method == 'POST':
                vals = request.POST
                brand = Brands.objects.get(id=int(vals['id'][0]))
                brand.name = vals['name']
                brand.logotype = vals['logotype']
                brand.save()
                brands = Brands.objects.all()
                return render(request, 'dashboard/components/brands.html', {'tab': 'brands', 'brands': brands})
            else:
                return JsonResponse('unsuccessful')
        else:
            if request.FILES:
                file_path = request.FILES['filetoupload'].temporary_file_path()
                filename = request.FILES['filetoupload'].name
                save_file(file_path, filename)
            brands = Brands.objects.all()
            return render(request, 'dashboard/index.html', {'tab': 'brands', 'brands': brands})


def models(request):
    if not request.user.is_superuser:
        return redirect('/cabinet/')
    else:
        models = Models.objects.order_by('name').all()
        m_length = len(models)
        try:
            limit = int(request.GET['limit'])
        except:
            limit = 20
        try:
            page = int(request.GET['page'])
        except:
            page = 1
        brands = Brands.objects.all()
        vendors = Vendors.objects.all()
        if request.is_ajax():
            if request.method == 'POST':
                vals = request.POST
                if vals['action'] == 'show_model':
                    mid = vals['mid']
                    model = _query(f'SELECT * FROM all_brand_models WHERE id = {mid};')
                    moduls = _query(f"""SELECT * FROM link_model_module_image lmmi 
                        LEFT JOIN dictionary_modules dm ON dm.id = lmmi.dictionary_module_id 
                        LEFT JOIN dictionary_module_image dmi ON dmi.id = lmmi.dictionary_module_image_id 
                        WHERE lmmi.model_id = {mid}""")
                    return render(request, 'dashboard/components/model_item.html',
                                  {'tab': 'models', 'model': str(model), 'brands': str(list(brands.values_list())),
                                   "moduls": str(moduls), "vendors": str(list(vendors.values_list()))})
                else:
                    try:
                        datas = json.loads(vals['data'])
                        mid = None
                        vendor = None
                        price = None
                        price_id = 0
                        name = None
                        main_image = None
                        image = None
                        brand_id = None

                        moid = None
                        module_name = None
                        module_description = None
                        module_scheme_picture = None
                        module_name_ru = None

                        moiid = None
                        module_image = None
                        for data in datas:
                            if 'model_name' in data['id']:
                                mid = data['id'].replace('model_name', '')
                                name = data['val']
                            if 'model_main_image' in data['id']:
                                main_image = data['val'].replace('/', '\\')
                            if 'model_image' in data['id']:
                                image = data['val'].replace('/', '\\')
                            if 'model_brand_name' in data['id']:
                                brand_id = int(data['val'])
                            if 'model_price' in data['id']:
                                price = data['val']
                            if 'price_id' in data['id']:
                                price_id = data['val']
                            if 'vendor_price' in data['id']:
                                vendor = data['val']
                            if 'module' in data['id']:
                                moid = data['id'].replace('module', '')
                                module_name = data['val']
                            if 'm_description' in data['id']:
                                module_description = data['val']
                            if 'm_scheme_picture' in data['id']:
                                module_scheme_picture = data['val']
                            if 'm_name_ru' in data['id']:
                                module_name_ru = data['val']
                            if moid is not None and module_name is not None and module_description is not None and module_name_ru is not None and module_scheme_picture is not None:
                                module_dict = DictionaryModules.objects.get(id=moid)
                                module_dict.name_en = module_name
                                module_dict.name_ru = module_name_ru
                                module_dict.save()
                                # module_spr.description = module_description
                                # module_spr.scheme_picture = module_scheme_picture
                                moid = None
                                module_name = None
                                module_description = None
                                module_scheme_picture = None
                                module_name_ru = None
                            if 'm_image' in data['id']:
                                moiid = data['id'].replace('m_image', '')
                                module_image = data['val']
                            if moiid is not None and module_image is not None:
                                module_image_dict = DictionaryModuleImage.objects.get(id=moiid)
                                module_image_dict.image = module_image
                                module_image_dict.save()
                                moiid = None
                                module_image = None
                        if price:
                            save_price(price, mid, vendor, 'model', price_id)
                        if mid is not None and name is not None and main_image is not None and image is not None and brand_id is not None:
                            model = Models.objects.get(id=mid)
                            model.name = name
                            model.brand_id = brand_id
                            model.main_image = main_image
                            model.image = image
                            model.save()
                            mid = None
                            name = None
                            main_image = None
                            image = None
                            brand_id = None
                    except:
                        pass
                    return render(request, 'dashboard/components/models.html',
                                  {'tab': 'models', 'models': str(list(models.values_list())), 'limit': int(limit),
                                   'page': int(page), 'm_length': m_length, 'brands': brands, 'vendors': str(vendors)})
            else:
                return JsonResponse('unsuccessful')
        return render(request, 'dashboard/index.html',
                      {'tab': 'models', 'models': str(list(models.values_list())), 'limit': int(limit),
                       'page': int(page),
                       'm_length': int(m_length / limit), 'brands': brands})


def partcodes(request):
    if not request.user.is_superuser:
        return redirect('/cabinet/')
    else:
        brands = Brands.objects.all()
        models = Models.objects.order_by('name').all()
        modules = DictionaryModules.objects.all()
        if request.is_ajax():
            if request.method == 'POST':
                vals = request.POST
                if vals['action'] == 'remove':
                    _query(f"""DELETE FROM link_model_module_partcode WHERE partcode_id = {int(vals['pid'])}
                        AND model_id = {int(vals['model_id'])} AND module_id = {int(vals['module_id'])}""")
                    partcode = _query(f"""SELECT p.id, p.code, p.images, p.article_code, p.description, 
                                            p.dictionary_partcode_id, b.id bid, b.name, dp.name_en, dp.name_ru, dp.image, dp.description_en, 
                                            dp.description_ru FROM partcodes p 
                                            LEFT JOIN dictionary_partcode dp ON dp.id = p.dictionary_partcode_id 
                                            LEFT JOIN brands b ON b.id = p.manufacturer 
                                            WHERE p.id = {int(vals['pid'])}""")
                    linking = _query(
                        f"""SELECT * FROM link_model_module_partcode WHERE partcode_id = {int(vals['pid'])}""")
                    return render(request, 'dashboard/components/partcode_item.html',
                                  {'tab': 'partcodes', 'partcode': str(partcode), 'linking': str(linking),
                                   'brands': str(list(brands.values_list())), 'models': str(list(models.values_list())),
                                   'modules': str(list(modules.values_list()))})
                if vals['action'] == 'show_partcode':
                    pid = vals['pid']
                    partcode = _query(f"""SELECT p.id, p.code, p.images, p.article_code, p.description, 
                        p.dictionary_partcode_id, b.id bid, b.name, dp.name_en, dp.name_ru, dp.image, dp.description_en, 
                        dp.description_ru FROM partcodes p 
                        LEFT JOIN dictionary_partcode dp ON dp.id = p.dictionary_partcode_id 
                        LEFT JOIN brands b ON b.id = p.manufacturer 
                        WHERE p.id = {pid}""")
                    linking = _query(f"""SELECT * FROM link_model_module_partcode WHERE partcode_id = {pid}""")
                    return render(request, 'dashboard/components/partcode_item.html',
                                  {'tab': 'partcodes', 'partcode': str(partcode), 'linking': str(linking),
                                   'brands': str(list(brands.values_list())), 'models': str(list(models.values_list())),
                                   'modules': str(list(modules.values_list()))})
                elif vals['action'] == 'search_partcode':
                    partcodes = _query(f"""SELECT * FROM partcodes WHERE code ILIKE '%{vals['val']}%'""")
                    return render(request, 'dashboard/components/partcode_list.html',
                                  {'tab': 'partcodes', 'partcodes': partcodes,
                                   'models': str(list(models.values_list())),
                                   'modules': str(list(modules.values_list()))})
                else:
                    partcode = Partcodes.objects.get(id=vals['pid'])
                    partcode.images = vals['partcode_image'].replace('/', '\\')
                    partcode.article_code = vals['partcode_article']
                    partcode.description = vals['partcode_desc']
                    partcode.save()
                    if vals['pid'] != '' and vals['module_id'] != '' and vals['module_id'] != '':
                        q = f"""INSERT INTO link_model_module_partcode(partcode_id, model_id, module_id)  
                                   VALUES ({int(vals['pid'])}, {int(vals['model_id'])}, {int(vals['module_id'])});"""
                        _query(q)
                    if vals['for_all'] == 'true':
                        dictionary_partcode_id = vals['dictionary_partcode_id']
                        dictionary_partcode = DictionaryPartcode.objects.get(id=dictionary_partcode_id)
                        dictionary_partcode.name_en = vals['partcode_name_en']
                        dictionary_partcode.name_ru = vals['partcode_name_ru']
                        dictionary_partcode.description_en = vals['partcode_desc_en']
                        dictionary_partcode.description_ru = vals['partcode_desc_ru']
                        dictionary_partcode.save()
                    partcode = _query(f"SELECT * FROM partcodes WHERE id = {vals['pid']};")
                    return render(request, 'dashboard/components/partcodes.html',
                                  {'tab': 'partcodes', 'partcode': str(partcode),
                                   'brands': str(list(brands.values_list())), 'models': str(list(models.values_list())),
                                   'modules': str(list(modules.values_list()))})
        partcodes = []
        return render(request, 'dashboard/index.html',
                      {'tab': 'partcodes', 'partcodes': partcodes, 'models': str(list(models.values_list())),
                       'modules': str(list(modules.values_list()))})


def modules(request):
    if not request.user.is_superuser:
        return redirect('/cabinet/')
    else:
        modules = DictionaryModules.objects.all()
        if request.is_ajax():
            if request.method == 'POST':
                vals = request.POST
                if vals['action'] == 'show_module':
                    module = DictionaryModules.objects.filter(id=int(vals['module_id']))
                    return render(request, 'dashboard/components/module_item.html',
                                  {'tab': 'modules', 'module': str(list(module.values_list()))})
                if vals['action'] == 'save':
                    module = DictionaryModules.objects.get(id=int(vals['module_id']))
                    module.name_en = vals['name_en']
                    module.name_ru = vals['name_ru']
                    module.save()
                    module = DictionaryModules.objects.filter(id=int(vals['module_id']))
                    return render(request, 'dashboard/components/module_item.html',
                                  {'tab': 'modules', 'module': str(list(module.values_list()))})
        return render(request, 'dashboard/index.html', {'tab': 'modules', 'modules': str(list(modules.values_list()))})


def prices(request):
    if not request.user.is_superuser:
        return redirect('/cabinet/')
    else:
        models = Models.objects.order_by('name').all()
        vendors = Vendors.objects.all()
        if request.is_ajax():
            if request.method == 'POST':
                vals = request.POST
                if vals['action'] == 'search_price':
                    q = f"""SELECT p.code, m.name model, v.name vendor, pr.* FROM prices pr
                            LEFT JOIN partcodes p ON p.id = pr.partcode_id
                            LEFT JOIN models m ON m.id = pr.model_id
                            LEFT JOIN vendors v ON v.id = pr.vendor_id
                            WHERE m.name ILIKE '%{vals['val']}%' or p.code ILIKE '%{vals['val']}%'"""
                    prices = _query(q)
                    return render(request, 'dashboard/components/price_list.html',
                                  {'tab': 'prices', 'prices': prices, 'models': str(list(models.values_list())),
                                   'vendors': str(list(vendors.values_list()))})
                if vals['action'] == 'search_add':
                    partcodes = _query(f"""SELECT * FROM partcodes WHERE code ILIKE '%{vals['val']}%';""")
                    prices = _query(f"""SELECT p.code, m.name model, v.name vendor, pr.* FROM prices pr
                                        LEFT JOIN partcodes p ON p.id = pr.partcode_id
                                        LEFT JOIN models m ON m.id = pr.model_id
                                        LEFT JOIN vendors v ON v.id = pr.vendor_id
                                        WHERE m.name ILIKE '%{vals['val']}%' or p.code ILIKE '%{vals['val']}%'""")
                    return render(request, 'dashboard/components/price_list.html',
                                  {'tab': 'prices', 'prices': prices, 'models': str(list(models.values_list())),
                                   'vendors': str(list(vendors.values_list())), 'partcodes': partcodes})
                if vals['action'] == 'show_price':
                    price = _query(f"""SELECT p.code, m.name model, v.name vendor, pr.* FROM prices pr
                                                LEFT JOIN partcodes p ON p.id = pr.partcode_id
                                                LEFT JOIN models m ON m.id = pr.model_id
                                                LEFT JOIN vendors v ON v.id = pr.vendor_id
                                                WHERE pr.id = {vals['id']}""")
                    return render(request, 'dashboard/components/price_item.html',
                                  {'tab': 'prices', 'price': price, 'models': str(list(models.values_list())),
                                   'vendors': str(list(vendors.values_list()))})
                if vals['action'] == 'new_price':
                    price = 'new'
                    if vals['type'] == 'model':
                        title = Models.objects.get(id=vals['id']).name
                    else:
                        title = Partcodes.objects.get(id=vals['id']).code
                    return render(request, 'dashboard/components/price_item.html',
                                  {'tab': 'prices', 'price': price, 'models': str(list(models.values_list())),
                                   'vendors': str(list(vendors.values_list())), 'ptype': vals['type'],
                                   'nid': vals['id'], 'title': title})
                if vals['action'] == 'add_price':
                    print(vals)
                    if vals['type'] == 'model':
                        model_id = int(vals['id'])
                        partcode_id = None
                        ids = f"(pr.model_id = {model_id} OR pr.partcode_id = NULL)"
                    else:
                        partcode_id = int(vals['id'])
                        model_id = None
                        ids = f"(pr.model_id = NULL OR pr.partcode_id = {partcode_id})"
                    try:
                        sprice = Prices(price=float(vals['price']), vendor_id=int(vals['vendor_id']),
                                        partcode_id=partcode_id, model_id=model_id,
                                        usage_status=vals['usage_status'], description=vals['description'],
                                        images=vals['images'], count=vals['count'])
                        sprice.save()
                    except Exception as err:
                        print(err)
                    price = _query(f"""SELECT p.code, m.name model, v.name vendor, pr.* FROM prices pr
                        LEFT JOIN partcodes p ON p.id = pr.partcode_id
                        LEFT JOIN models m ON m.id = pr.model_id
                        LEFT JOIN vendors v ON v.id = pr.vendor_id
                        WHERE pr.vendor_id = {int(vals['vendor_id'])} AND pr.price = {float(vals['price'])} AND  
                        {ids}""")
                    print(price)
                    return render(request, 'dashboard/components/price_item.html',
                                  {'tab': 'prices', 'price': price, 'models': str(list(models.values_list())),
                                   'vendors': str(list(vendors.values_list()))})
                if vals['action'] == 'save':
                    sprice = Prices.objects.get(id=vals['id'])
                    sprice.price = float(vals['price'])
                    sprice.vendor_id = int(vals['vendor_id'])
                    sprice.usage_status = vals['usage_status']
                    sprice.description = vals['description']
                    sprice.images = vals['images']
                    sprice.count = int(vals['count'])
                    sprice.save()
                    price = _query(f"""SELECT p.code, m.name model, v.name vendor, pr.* FROM prices pr
                            LEFT JOIN partcodes p ON p.id = pr.partcode_id
                            LEFT JOIN models m ON m.id = pr.model_id
                            LEFT JOIN vendors v ON v.id = pr.vendor_id
                            WHERE pr.id = {vals['id']}""")
                    return render(request, 'dashboard/components/price_item.html',
                                  {'tab': 'prices', 'price': price, 'models': str(list(models.values_list())),
                                   'vendors': str(list(vendors.values_list()))})
        return render(request, 'dashboard/index.html', {'tab': 'prices', 'models': str(list(models.values_list()))})
