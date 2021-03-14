from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    PasswordResetView, LoginView, PasswordChangeView, PasswordResetConfirmView, LogoutView
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


class Login(LoginView):
    template_name = 'users/authForm.html'
    redirect_authenticated_user = True

    # def get_success_url(self):
    #     return reverse_lazy('index')


class PasswordReset(PasswordResetView):
    template_name = 'users/resetPassword.html'


def password_reset_done(request):
    message = 'Проверьте свою почту, там наверняка лежит ссылка на смену пароля ^_^'
    return render(request, 'users/customPage.html', {'message': message})


class PasswordResetConfirmation(PasswordResetConfirmView):
    template_name = 'users/resetPasswordForm.html'


def password_reset_complete(request):
    message = 'Смена пароля прошла успешно! Постарайтесь больше не терять ^_^'
    return render(request, 'users/customPage.html', {'message': message})


class PasswordChange(PasswordChangeView):
    template_name = 'users/changePassword.html'


class Logout(LogoutView):
    next_page = reverse_lazy('index')






