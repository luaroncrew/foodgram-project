from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.registration, name='signup'),
    path('password-reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password-reset-done/', views.password_reset_done, name='password_reset_done'),
    path('login/', views.Login.as_view(), name='login'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmation.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.password_reset_complete, name='password_reset_complete')
]