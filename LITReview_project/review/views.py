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
    reviews = Review.objects.all()  # get_users_viewable_reviews()
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = Ticket.objects.all()  # get_users_viewable_tickets()
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
        prepare_save.user = request.user
        prepare_save.save()
        r = True

    return r


@login_required
def ticket(request, ticket_edit_id=None, ticket_delete_id=None):
    """
        Fonction de gestion des demande de critiques appelé Ticket
    """
    if ticket_delete_id and request.method == 'GET':  # Suppression d'un ticket
        to_delete = get_object_or_404(Ticket, id=ticket_delete_id)
        to_delete.delete()
        return redirect(index)
    elif ticket_edit_id:  # Edition d'un ticket
        to_edit = get_object_or_404(Ticket, id=ticket_edit_id)
        form = TicketForm(instance=to_edit)
        if request.method == 'POST':
            form = TicketForm(request.POST, request.FILES, instance=to_edit)

            if validate_form(form, request):
                return redirect(index)

    elif request.method == 'POST':  # Création d'un ticket
        form = TicketForm(request.POST, request.FILES)

        if validate_form(form, request):
            return redirect(index)

    else:  # Affichage d'un formulaire vierge pour créer un ticket
        form = TicketForm()

    context = {'title': ' - Demander une critique',
               'form':  form
               }
    return render(request, 'review/ticket.html', context)


@login_required
def review(request, ticket_id=None, review_edit_id=None, review_delete_id=None):
    """
        Fonction de gestion des Critiques
    """
    title_html = ' - Créer une critique'
    if review_delete_id and request.method == 'GET':  # Suppression d'une critique
        to_delete = get_object_or_404(Review, id=review_delete_id)
        to_delete.delete()
        return redirect(index)

    elif ticket_id and request.method == 'POST':  # Création d'une critique en réponse a un ticket
        form_review = ReviewForm(request.POST)

        if form_review.is_valid():
            insert = form_review.save(commit=False)
            insert.ticket_id = ticket_id
            insert.user = request.user
            insert.save()

        return redirect(index)

    elif review_edit_id:  # Edition d'une critique
        title_html = ' - Editer une critique'
        review_to_edit = get_object_or_404(Review, id=review_edit_id)
        form_review = ReviewForm(instance=review_to_edit)
        ticket_to_edit = get_object_or_404(Ticket, id=review_to_edit.ticket.pk)
        form_ticket = TicketForm(instance=ticket_to_edit)

        if request.method == 'POST':
            form_ticket = TicketForm(request.POST, request.FILES, instance=ticket_to_edit)
            form_review = ReviewForm(request.POST, instance=review_to_edit)
            validate_form(form_ticket, request)
            if form_review.is_valid():
                form_review.save()
            return redirect(index)

    # Affichage formulaire pour répondre a un ticket par une critique
    elif ticket_id and request.method == 'GET':
        title_html = ' - Créer une critique'
        to_answer = get_object_or_404(Ticket, id=ticket_id)
        form_ticket = TicketForm(instance=to_answer)
        form_review = ReviewForm()

    elif request.method == 'POST':
        form_ticket = TicketForm(request.POST, request.FILES)

        if validate_form(form_ticket, request):
            form_review = ReviewForm(request.POST)
            insert = form_review.save(commit=False)
            insert.ticket_id = Ticket.objects.get(title=request.POST["title"], user_id=request.user).id
            insert.user = request.user
            insert.save()

        return redirect(index)

    else:
        form_ticket = TicketForm()
        form_review = ReviewForm()

    context = {'title':       title_html,
               'form_review':  form_review,
               'form_ticket': form_ticket
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
            'form':  form
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
    if request.method == 'GET' and delete_id is not None:
        r = get_object_or_404(UserFollows.objects.filter(user_id=request.user.id,
                                                         followed_user_id=delete_id))
        if r:
            r.delete()
            return redirect('abonnement')

    elif request.method == 'POST':
        form = FollowerForm(request.POST)

        if validate_form(form, request):
            return redirect('abonnement')

    else:
        followed = UserFollows.objects.filter(user_id=request.user.id)
        followers = UserFollows.objects.filter(followed_user_id=request.user.id)
        form = FollowerForm()

    context = {'title':     ' - Demander une critique',
               'form':      form,
               'followed':  followed,
               'followers': followers
               }

    return render(request, 'review/follow.html', context)
