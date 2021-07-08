from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout

from functions.filter_func import select_cart_items, remove_cart_item, change_cart_count, order_cart, get_orders
from user_passport.functions import get_profile, save_profile


def cabinet(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login/')
    else:
        order = None
        if request.POST and 'csrfmiddlewaretoken' in request.POST:
            user = User.objects.get(username=request.user.username)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            save_profile(request.POST['address'], request.POST['phone'], request.user)
            if request.POST['password'] == request.POST['repassword'] and len(request.POST['password']) > 6:
                user.password = request.POST['password']
            user.save()
            request.user = User.objects.get(username=request.user.username)
        lang = request.LANGUAGE_CODE
        if 'changecart' in request.POST:
            if request.POST['action'] == 'remove':
                remove_cart_item(request.POST['pid'], request.user.id)
            if request.POST['action'] == 'count':
                change_cart_count(request.POST['pid'], request.user.id, request.POST['value'])
        if 'order' in request.POST:
            order = order_cart(request)
        cart_items = select_cart_items(request.user.id, 'true')
        cart_count = len(cart_items)
        cart_summa = 0
        orders = get_orders(request)
        for item in cart_items:
            cart_summa += float(item[4]) * item[3]
        profile = get_profile(request.user)[0]
        context = {
            'lang': lang,
            'cart_count': cart_count,
            'cart_items': cart_items,
            'cart_summa': cart_summa,
            'user': request.user,
            'profile': profile,
            'order': order,
            'orders': orders
        }

        if 'tab' in request.GET:
            if 'profile' in request.GET['tab']:
                context.update({'tab': 'profile'})
                return render(request, 'cabinet/index.html', context)
            elif 'favorite' in request.GET['tab']:
                context.update({'tab': 'favorite'})
                return render(request, 'cabinet/index.html', context)
            else:
                if request.is_ajax():
                    context.update({'tab': 'cart'})
                    return render(request, 'cabinet/cart.html', context)
                else:
                    context.update({'tab': 'cart'})
                    return render(request, 'cabinet/index.html', context)
        else:
            if request.is_ajax():
                context.update({'tab': 'cart'})
                return render(request, 'cabinet/cart.html', context)
            else:
                context.update({'tab': 'cart'})
                return render(request, 'cabinet/index.html', context)


def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            if request.recaptcha_is_valid:
                form = request.POST
                username = form['username']
                password = form['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    # the password verified for the user
                    if user.is_active:
                        auth_login(request, user)
                        return redirect('/cabinet/')
                    else:
                        return render(request, 'registration/login.html')
                else:
                    return render(request, 'registration/login.html', context={'error': 'Wrong username or password',
                                                                               'error_ru': 'Не верное имя или пароль'})
            else:
                return render(request, 'registration/login.html')
        else:
            return render(request, 'registration/login.html')
    else:
        return render(request, 'cabinet/index.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('/cabinet/')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)
