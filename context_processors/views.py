def main_menu(request):
    path = str(request.path)
    menu_list = [
        ['/', 'Главная']
        , ['/brand/brands/', 'Бренды и модели']
        , ['/supplies/', 'Расходные материалы']
        # , ['/about/', 'О нас']
    ]

    menu_auth = [
        ['/', 'Вход'],
        ['/', 'Выход']
    ]
    try:
        if 'brand' in path or 'model' in path:
            cur_item = 'Бренды и модели'
        elif 'supplies' in path:
            cur_item = 'Расходные материалы'
        else:
            cur_item = 'Главная'
    except KeyError as e:
        cur_item = 'Главная'
    return {'menu_list': menu_list, 'menu_item_active': cur_item, 'menu_auth': menu_auth}
