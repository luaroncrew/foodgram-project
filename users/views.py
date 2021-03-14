from django.shortcuts import render, redirect
from django.contrib.auth.views import (
PasswordResetView, LoginView, PasswordChangeView, PasswordResetConfirmView
)
from django.contrib.auth.forms import(
    PasswordResetForm, AuthenticationForm, PasswordChangeForm,
)
from django.urls import reverse_lazy
from .forms import CreationForm


def registration(request):
    form = CreationForm()
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'users/reg.html', context)


def password_reset_done(request):
    message = 'Проверьте свою почту, там наверняка лежит ссылка на смену пароля'
    return render(request, 'users/customPage.html', context={'message': message})


class PasswordReset(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'users/resetPassword.html'
    success_url = reverse_lazy('password_reset_done')


class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'users/changePassword.html'


class Login(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/authForm.html'

    def get_success_url(self):
        return reverse_lazy('index')


class PasswordResetConfirmation(PasswordResetConfirmView):
    template_name = 'users/resetPasswordForm.html'


def password_reset_complete(request):
    message = 'смена пароля прошла успешно'
    return render(request, 'users/customPage.html', context={'message': message})








