from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _('Пароли не совпадают')
    }

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']
