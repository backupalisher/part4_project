from django.shortcuts import render

# Create your views here.
def main_menu(request):
    path = str(request.path)
    curItem = 'Главная'
    menuList = [
        ['/', 'Главная'],
        ['/brand/brands', 'Бренды'],
        ['/contacts', 'Контакты'],
        ['/about', 'О нас']
    ]

    menuAuth = [
        ['/', 'Вход'],
        ['/', 'Выход']
    ]
    try:
        for menu in menuList:
            if menu[0] == path:
                curItem = menu[1]
    except KeyError as e:
        curItem = 'Главная'
    return {'menu_list': menuList, 'menu_item_active': curItem, 'menu_auth': menuAuth}