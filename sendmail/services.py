from django.core.mail import send_mail
from django.template.loader import render_to_string


def send(request):
    import socket
    soc = socket.getaddrinfo('smtp.gmail.com', 587)
    print(soc)
    user_mail = 'info@part4.info'
    data = request.POST
    msg = data['title'] + ' код: ' + data['product_code'] + ' с id: ' + data['product_id'] + '\n' + \
          'От ' + data['name'] + ' ' + data['phone'] + ' ' + data['email']
    print(msg)
    send_mail(
        'Новый заказ',
        msg,
        'info@part4.info',
        [user_mail],
        fail_silently=False,
    )

