from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView

from django.db.models import CharField, Value
from .forms import Register, Connect, TicketForm, ReviewForm, FollowerForm
from .models import Ticket, Review, UserFollows


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
    reviews = Review.objects.all() # get_users_viewable_reviews()
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = Ticket.objects.all() # get_users_viewable_tickets()
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

def validate_form(form, request):
    r = False
    if form.is_valid:
        prepare_save = form.save(commit=False)
        prepare_save.user  = request.user
        prepare_save.save()
        r = True

    return r

@login_required
def ticket(request, ticket_id=None):
    if ticket_id and request.method == 'GET':
        res =  get_object_or_404(Ticket, id=ticket_id)
        form = TicketForm(res)
    elif request.method == 'POST':
        form = TicketForm(request.POST)

        if validate_form(form,request):
            return redirect(index)

    else:
        form = TicketForm()

    context = {'title': ' - Demander une critique',
               'form': form
               }
    return render(request, 'review/ticket.html', context)


@login_required
def review(request, review_id=None):
    if review_id and request.method == 'GET':
        res =  get_object_or_404(Review, id=review_id)

    elif request.method == 'POST':
        form_Review = ReviewForm(request.POST)
        form_Ticket = TicketForm(request.POST)

        if validate_form(form_Ticket, request):
            if validate_form(form_Review, request):
                return redirect(index)
    else:
        form_Review = ReviewForm()
        form_Ticket = TicketForm()

    context = {'title': ' - Créer une critique',
               'form_Review': form_Review,
               'form_Ticket': form_Ticket
               }
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

@login_required
def personal_post(request):
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

    return render(request, 'review/post.html', context)

@login_required
def followers(request, delete_id=None):
    if request.method == 'GET' and delete_id != None:
        r = get_object_or_404(UserFollows.objects.filter(user_id=request.user.id, followed_user_id=delete_id))
        if r:
            r.delete()
            return redirect('abonnement')

    elif request.method == 'POST':
        form = FollowerForm(request.POST)

        if validate_form(form,request):
            return redirect('abonnement')

    else:
        followed = UserFollows.objects.filter(user_id=request.user.id )
        followers = UserFollows.objects.filter(followed_user_id=request.user.id )
        form = FollowerForm()

    context = {'title': ' - Demander une critique',
               'form': form,
               'followed': followed,
               'followers': followers
               }

    return render(request, 'review/follow.html', context)