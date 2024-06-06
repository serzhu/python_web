
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.urls import reverse_lazy
from .forms import EmailPasswordResetForm, RegisterForm, LoginForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView


def signupuser(request:HttpRequest):
    if request.user.is_authenticated:
        return redirect(to='app_quotes:quotes')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect(to='app_auth:login')
        else:
            return render(request, 'app_auth/signup.html', context={"form": form})

    return render(request, 'app_auth/signup.html', context={"form": RegisterForm()})


def loginuser(request:HttpRequest):
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


class AppPasswordResetView(PasswordResetView):
    form_class = EmailPasswordResetForm
    template_name = 'app_auth/password_reset_form.html'
    email_template_name = 'app_auth/password_reset_email.html'
    subject_template_name = 'app_auth/password_reset_subject.txt'
    from_email = 'serhii.zhukov@ukr.net'
    success_url = reverse_lazy('app_auth:password_reset_done')

class AppPasswordResetDoneView(PasswordResetDoneView):
    template_name="app_auth/password_reset_done.html"

class AppPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'app_auth/password_reset_confirm.html'
    success_url = reverse_lazy('app_auth:password_reset_complete')

class AppPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'app_auth/password_reset_complete.html'

  