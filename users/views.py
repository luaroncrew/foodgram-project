from django.contrib.auth.views import (
    PasswordResetView,
    LoginView,
    PasswordChangeView,
    PasswordResetConfirmView,
    LogoutView
)
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import CreationForm


def registration(request):
    form = CreationForm()
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('index')
    context = {'form': form}
    return render(request, 'users/reg.html', context)


class Login(LoginView):
    template_name = 'users/authForm.html'
    redirect_authenticated_user = True


class PasswordReset(PasswordResetView):
    template_name = 'users/resetPassword.html'


def password_reset_done(request):
    message = ('Проверьте свою почту,'
               ' там наверняка лежит ссылка на смену пароля ^_^')
    return render(request, 'users/message_page.html', {'message': message})


class PasswordResetConfirmation(PasswordResetConfirmView):
    template_name = 'users/resetPasswordForm.html'


def password_reset_complete(request):
    message = 'Смена пароля прошла успешно! ^_^'
    return render(request, 'users/message_page.html', {'message': message})


class PasswordChange(PasswordChangeView):
    template_name = 'users/changePassword.html'
    success_url = reverse_lazy('password_reset_complete')


class Logout(LogoutView):
    next_page = reverse_lazy('index')
