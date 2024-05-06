from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm


def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='app_quotes:quotes')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='app_quotes:quotes')
        else:
            return render(request, 'app_auth/signup.html', context={"form": form})

    return render(request, 'app_auth/signup.html', context={"form": RegisterForm()})

def loginuser(request):
    if request.user.is_authenticated:
       return redirect(to='app_quotes:quotes')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='app_auth:login')

        login(request, user)
        return redirect(to='app_quotes:quotes')

    return render(request, 'app_auth/login.html', context={"form": LoginForm()})

@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='app_quotes:quotes')

