from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect


def login(request):
    return render(request, 'user_passport/index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('registration/index.html')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)
