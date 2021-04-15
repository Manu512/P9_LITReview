from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class Register(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
                {'placeholder': 'Nom d\'utilisateur', 'size':40}
        )
        self.fields['password1'].widget.attrs.update({'placeholder': 'Mot de passe', 'size':40})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmer le mot de passe',
                                                      'size':40})

class Connect(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
                {'placeholder': 'Nom d\'utilisateur', 'size':60}
        )
        self.fields['password'].widget.attrs.update({'placeholder': 'Mot de passe', 'size':60})
