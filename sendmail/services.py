from django.core.mail import send_mail
from django.template.loader import render_to_string
import socket

# soc = socket.getaddrinfo('smtp.yandex.ru', 465)
soc = socket.getaddrinfo('smtp.gmail.com', 587)


def send(request):
    user_mail = 'info@part4.info'
    data = request.POST
    msg = 'От ' + data['name'] + ' ' + data['phone'] + ' ' + data['email'] + '\n' + data['message']
    print(msg)
    send_mail(
        'Сообщение от ' + data['name'],
        msg,
        'info@part4.info',
        [user_mail],
        fail_silently=False,
    )


def send_contact(request):
    user_mail = 'info@part4.info'
    data = request.POST
    msg = 'От ' + data['name'] + ' ' + data['phone'] + ' ' + data['email'] + '\n' + data['message']
    print(msg)
    send_mail(subject='Новый заказ от ' + data['name'], message=msg, from_email='info@part4.info',
              recipient_list=[user_mail], fail_silently=False)
