from itertools import chain

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView

from django.db.models import CharField, Value
from .forms import Register, Connect
from .models import Ticket, Review


# Create your views here.

class Login(LoginView):
    """ Class in order to change login form"""

    template_name = 'review/login.html'
    authentication_form = Connect
    extra_context = {'title': ' - Accueil'}


def get_users_viewable_reviews(user):
    return Review.objects.filter(user=user)


def get_users_viewable_tickets(user):
    return Ticket.objects.filter(user=user)


@login_required
def index(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
    )
    context = {'title': ' - Flux',
               'posts': posts}

    return render(request, 'review/index.html', context)


@login_required
def ticket(request):
    context = {'title': ' - Demander une critique'}
    return render(request, 'review/ticket.html', context)


@login_required
def review(request):
    context = {'title': ' - Créer une critique'}
    return render(request, 'review/review.html', context)


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
            'title': ""' - Inscription'"",
            'form': form
    }
    return render(request, 'review/register.html', context)
