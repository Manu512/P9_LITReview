from django.forms import ModelForm, TextInput, EmailInput
from .models import UserFollows
from django.contrib.auth.models import User


class LoginUser(ModelForm):
    pass