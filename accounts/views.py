from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'accounts/register.html', {'form': form})
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        print(username, password)
        auser = authenticate(username=username, password=password)
        print(auser)
        if auser is not None:
            login(request, auser)
        else:
            user = User.objects.create_user(username=username, email='', password=password)
            print('test')
            auser = authenticate(username=username, password=password)
            login(request, auser)
        return redirect('/accounts/profile')
    else:
        form = UserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})
