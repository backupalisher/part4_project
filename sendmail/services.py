import json

from django.core.mail import send_mail
from django.template.loader import render_to_string
import socket

# soc = socket.getaddrinfo('smtp.yandex.ru', 465)
soc = socket.getaddrinfo('smtp.gmail.com', 587)


def send(request, order):
    company_mail = 'info@part4.info'
    # company_mail = 'aresy@yandex.ru'
    data = request.POST
    msg = 'От ' + data['first_name'] + ' ' + data['last_name'] + ' на сумму ' + data['summ'] + '\n' \
          + data['phone'] + '\n' + data['email'] + '\n' + data['address'] + '\n' + 'Заказ: ' + '\n'
    for item in json.loads(data['cart_items']):
        msg += item['orders'] + ' (id: ' + str(item['partcode_id']) + str(item['model_id']) + ') ' \
               + str(item['count']) + ' шт. по цене ' + item['price'] + '\n'
    msg += 'Общая сумма: ' + data['summ']
    send_mail(
        'Заказ № ' + order + ' от ' + data['first_name'] + ' на сумму ' + data['summ'],
        msg,
        'info@part4.info',
        [company_mail],
        fail_silently=False,
    )
    # if data['email']:
    #     user_mail = data['email']
    #     send_mail(
    #         'Заказ ',
    #         msg,
    #         'info@part4.info',
    #         [user_mail],
    #         fail_silently=False,
    #     )


def send_contact(request):
    user_mail = 'info@part4.info'
    data = request.POST
    msg = 'Заказ http://part4.info' + data['url'].replace('"', '') + '\n' +\
          'От ' + data['name'] + ' ' + data['phone'] + ' ' + data['email'] + '\n' + data['message']
    print(msg)
    send_mail(subject='Новый заказ от ' + data['name'], message=msg, from_email='info@part4.info',
              recipient_list=[user_mail], fail_silently=False)
