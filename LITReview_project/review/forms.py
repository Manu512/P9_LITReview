"""forms.py"""
from django.contrib.auth.models import User
from django.forms import RadioSelect, Textarea
from django.forms.models import ModelForm

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Review, Ticket, UserFollows


class Register(UserCreationForm):
    """
    Formulaire d'enregistrement de l'utilisateur hérite de UserCreationForm.
    """
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
                {'placeholder': 'Nom d\'utilisateur', 'size': 40}
        )
        self.fields['password1'].widget.attrs.update({'placeholder': 'Mot de passe', 'size': 40})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmer le mot de passe',
                                                      'size':        40})


class Connect(AuthenticationForm):
    """
    Formulaire d'authentification de l'utilisateur hérite de AuthenticationForm.
    """
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Nom d\'utilisateur', 'size': 60})
        self.fields['password'].widget.attrs.update({'placeholder': 'Mot de passe', 'size': 60})


class TicketForm(ModelForm):
    """
    Définition du formulaire du ticket (TICKET) qui hérite de l'objet ModelForm.
    """
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        labels = {
                "title":       "Titre",
                "description": "Description",
                "image":       "Image"
        }


class ReviewForm(ModelForm):
    """
    Définition du formulaire des critiques (REVIEW) qui hérite de l'objet ModelForm.
    """
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        labels = {
                "rating":   "Note",
                "headline": "Titre",
                "body":     "Commentaire",
        }
        widgets = {
                "rating": RadioSelect(
                    choices=((0, "- 0"), (1, "- 1"), (2, "- 2"), (3, "- 3"), (4, "- 4"), (5, "- 5"))),
                "body":   Textarea()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'special'})


class FollowerForm(ModelForm):
    """
    Définition du formulaire des abonnements (Followers) suivi des utilisateurs qui hérite de l'objet ModelForm.
    """
    class Meta:
        model = UserFollows
        fields = ["followed_user"]
        labels = {
                "followed_user": "Nom d'utilisateurs",
        }
