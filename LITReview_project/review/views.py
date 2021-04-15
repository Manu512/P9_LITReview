from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import Register, Connect


# Create your views here.

class Login(LoginView):
    """ Class in order to change login form"""

    templates_name = 'registration/login.html'
    authentication_form = Connect


@login_required
def index(request):
    context = { 'test': 'context'}
    return render(request, 'review/index.html', context)


def register(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            messages.success(request, "L'utilisateur " + user_name + ' a été enregistré')
            return redirect('login')
    else:
        form = Register()

    context = {
            'form': form
    }
    return render(request, 'review/register.html', context)
