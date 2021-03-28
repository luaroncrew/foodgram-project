from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, PasswordInput
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class CreationForm(UserCreationForm):
    password2 = None
    password1 = CharField(
        label=_("пароль"),
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1']
        labels = {
            'first_name': _('ваше имя'),
            'username': _('имя пользователя'),
            'email': _('электронный адрес'),
        }
