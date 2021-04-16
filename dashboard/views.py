import json

import boto3
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import render
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
    print(type(file_path), file_path)
    print(type(filename), filename)
    print(type(aws_bucket), aws_bucket)
    print(type(aws_access_key_id), aws_access_key_id)
    print(type(aws_secret_access_key), aws_secret_access_key)
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


@staff_member_required
def index(request):
    return render(request, 'dashboard/index.html', {'tab': 'index'})


@staff_member_required
def brands(request):
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


@staff_member_required
def models(request):
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
                moduls = _query(f'SELECT * FROM link_model_module_image lmmi '
                                f'LEFT JOIN spr_modules sm ON sm.id = lmmi.spr_module_id '
                                f'LEFT JOIN spr_module_image smi ON smi.id = lmmi.spr_module_image_id '
                                f'WHERE lmmi.model_id = {mid}')
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
                            module_spr = SprModules.objects.get(id=moid)
                            module_spr.name = module_name
                            module_spr.description = module_description
                            module_spr.scheme_picture = module_scheme_picture
                            module_spr.name_ru = module_name_ru
                            module_spr.save()
                            moid = None
                            module_name = None
                            module_description = None
                            module_scheme_picture = None
                            module_name_ru = None
                        if 'm_image' in data['id']:
                            moiid = data['id'].replace('m_image', '')
                            module_image = data['val']
                        if moiid is not None and module_image is not None:
                            spr_module_image = SprModuleImage.objects.get(id=moiid)
                            spr_module_image.image = module_image
                            spr_module_image.save()
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
                  {'tab': 'models', 'models': str(list(models.values_list())), 'limit': int(limit), 'page': int(page),
                   'm_length': int(m_length / limit), 'brands': brands})


@staff_member_required
def partcodes(request):
    brands = Brands.objects.all()
    vendors = Vendors.objects.all()
    if request.is_ajax():
        if request.method == 'POST':
            vals = request.POST
            if vals['action'] == 'show_partcode':
                pid = vals['pid']
                partcode = []
                qpartcode = _query(f'SELECT * FROM partcodes WHERE id = {pid};')
                price = _query(f'SELECT price, vendor_id, id FROM prices WHERE partcode_id = {pid};')
                partcode.append(qpartcode)
                partcode.append(price)
                return render(request, 'dashboard/components/partcode_item.html',
                              {'tab': 'partcodes', 'partcode': str(partcode),
                               "vendors": str(list(vendors.values_list())), 'brands': str(list(brands.values_list()))})
            else:
                partcode = []
                pid = vals['pid']
                partcode_desc = vals['partcode_desc']
                partcode_image = vals['partcode_image'].replace('/', '\\')
                partcode_article = vals['partcode_article']
                mpartcode = Partcodes.objects.get(id=pid)
                mpartcode.description = partcode_desc
                mpartcode.images = partcode_image
                mpartcode.article_code = partcode_article
                mpartcode.save()
                detail_price = vals['detail_price']
                vendor = vals['vendor']
                if vals['price_id']:
                    price_id = vals['price_id']
                else:
                    price_id = 0
                save_price(detail_price, pid, vendor, 'partcode', price_id)
                _query(f"UPDATE partcodes SET (description, images, article_code) = ('{partcode_desc}',"
                       f"'{partcode_image}', '{partcode_article}') WHERE id = 55158")
                partcode = _query(f'SELECT * FROM partcodes WHERE id = {pid};')
                price = _query(f'SELECT price, vendor_id, id FROM prices WHERE partcode_id = {pid};')
                partcode.append(partcode)
                partcode.append(price)
                return render(request, 'dashboard/components/partcodes.html',
                              {'tab': 'partcodes', 'partcode': str(partcode),
                               'brands': str(list(brands.values_list()))})
    partcodes = _query(f"SELECT * FROM all_partcodes ORDER BY id")
    return render(request, 'dashboard/index.html', {'tab': 'partcodes', 'partcodes': partcodes})


@staff_member_required
def details(request):
    details = _query(f'SELECT d.id d_id, sd.*, sm.name module, p.detail_id, p.price, p.usage_status, p.vendor_id, p.id '
                     f'FROM details d LEFT JOIN spr_details sd ON sd.id = d.spr_detail_id '
                     f'LEFT JOIN spr_modules sm ON sm.id = d.module_id LEFT JOIN prices p ON p.detail_id = d.id '
                     f'WHERE d.partcode_id is NULL and d.module_id is not NULL')
    partcodes = _query(f"SELECT * FROM all_partcodes ORDER BY id")
    vendors = Vendors.objects.all()
    if request.is_ajax():
        if request.method == 'POST':
            vals = request.POST
            if vals['action'] == 'show_detail':
                detail = None
                for item in details:
                    if int(vals['did']) == int(item[0]):
                        detail = item
                return render(request, 'dashboard/components/detail_item.html',
                              {'tab': 'details', 'partcode': str(detail), 'partcodes': str(partcodes),
                               "vendors": str(list(vendors.values_list()))})
            if vals['action'] == 'save':
                did = vals['did']
                spr_id = vals['spr_id']
                detail_name = vals['detail_name']
                description = vals['description']
                seo = vals['seo']
                base_img = vals['base_img']
                detail_price = vals['detail_price']
                use_status = vals['use_status']
                partcode = vals['partcode']
                vendor = vals['vendor']
                price_id = 0
                if detail_name != '' or description != '' or base_img != '' or seo != '' or detail_price != '' or use_status != '':
                    qspr_detail = SprDetails.objects.get(id=spr_id)
                    qspr_detail.name_ru = detail_name
                    qspr_detail.description = description
                    qspr_detail.seo = seo
                    qspr_detail.base_img = base_img
                    qspr_detail.save()
                if partcode != '':
                    qdetail = Details.objects.get(id=did)
                    qdetail.partcode_id = partcode
                    qdetail.save()
                if detail_price != '':
                    if vals['price_id']:
                        price_id = vals['price_id']
                    save_price(detail_price, did, vendor, 'partcode', price_id)

                return render(request, 'dashboard/index.html', {'tab': 'details', 'details': details})
    return render(request, 'dashboard/index.html', {'tab': 'details', 'details': details})
