""" views.py """
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


def get_users_viewable_reviews(user: list):
    """
    Fonction qui récupère et affiche les critiques d'une liste utilisateurs (qui sont suivis)
    :param user: liste des utilisateurs suivi.
    :return: Object Review
    """
    return Review.objects.filter(user__in=user)


def get_users_viewable_tickets(user):
    """
    Fonction qui récupère et affiche les tickets d'une liste utilisateurs (qui sont suivis)
    :param user: liste des utilisateurs suivi.
    :return: Object Ticket
    """
    return Ticket.objects.filter(user__in=user)


@login_required
def index(request):
    """
    Fonction qui affiche/génère la page index à condition d'etre authentifié
    :return: Template index
    """
    to_show = [request.user.pk]
    if request.path == '/':
        title = ' - Flux '
        to_show = to_show + list(
            UserFollows.objects.filter(user=request.user.id).values_list('followed_user_id', flat=True))

    elif request.path == '/post/':
        title = ' - Posts Personnel'

    ticket_with_reply = []
    reviews = get_users_viewable_reviews(to_show)
    for response in reviews:
        ticket_with_reply.append(response.ticket)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(to_show)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
    )
    context = {'title': title,
               'posts': posts,
               'ticket_with_reply': ticket_with_reply
               }

    return render(request, 'review/index.html', context)


def validate_form(form, request, ticket_id=None):
    """
    Fonction de contrôle et de validation des formulaires et gestion de critiques lié a un ticket.
    :param form: obj Form (Formulaire)
    :param request: obj request
    :param ticket_id: si défini obj int qui contient l'id du ticket à lié a la critique.
    :return: Bool True si Valid
    """
    valid = False
    if form.is_valid():
        prepare_save = form.save(commit=False)
        if ticket_id:
            prepare_save.ticket_id = ticket_id
        prepare_save.user = request.user
        prepare_save.save()
        valid = True
    return valid


@login_required
def ticket(request, ticket_edit_id=None, ticket_delete_id=None):
    """
        Fonction de gestion et d'affichage des demande de critiques appelé Ticket
        :param request:
        :param ticket_edit_id: Si défini id du ticket à éditer.
        :param ticket_delete_id: Si défini id du ticket à supprimer.
        :return: Informations a afficher dans le template ticket.html
    """
    if ticket_delete_id and request.method == 'GET':  # Suppression d'un ticket
        to_delete = get_object_or_404(Ticket, id=ticket_delete_id)
        to_delete.delete()
        return redirect(index)
    elif ticket_edit_id:  # Edition d'un ticket
        title_html = " - Edition d'une demande de critique"
        to_edit = get_object_or_404(Ticket, id=ticket_edit_id)
        form = TicketForm(instance=to_edit)
        if request.method == 'POST':
            form = TicketForm(request.POST, request.FILES, instance=to_edit)
            validate_form(form, request)
            return redirect(index)

    elif request.method == 'POST':  # Création d'un ticket
        form = TicketForm(request.POST, request.FILES)
        validate_form(form, request)
        return redirect(index)

    else:  # Affichage d'un formulaire vierge pour créer un ticket
        title_html = ' - Demander une critique'
        form = TicketForm()

    context = {'title': title_html,
               'form':  form
               }
    return render(request, 'review/ticket.html', context)


@login_required
def review(request, ticket_id=None, review_edit_id=None, review_delete_id=None):
    """
        Fonction de gestion et d'affichage des Critiques
        :param request:
        :param ticket_id: défini lorsque l'ont crée une critique en réponse à un ticket précis.
        :param review_edit_id: si défini on modifie la critique défini par l'id.
        :param review_delete_id: si défini on supprime la critique défini par l'id.
        :return: Informations à afficher dans le template review.html
    """
    title_html = ' - Créer une critique'
    if review_delete_id and request.method == 'GET':  # Suppression d'une critique
        get_object_or_404(Review, id=review_delete_id).delete()
        return redirect(index)

    elif ticket_id and request.method == 'POST':  # Création d'une critique en réponse a un ticket
        form_review = ReviewForm(request.POST)
        validate_form(form_review, request, ticket_id)
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
            validate_form(form_review, request)
            return redirect(index)

    # Affichage formulaire pour répondre a un ticket par une critique
    elif ticket_id and request.method == 'GET':
        title_html = ' - Créer une critique'
        to_answer = get_object_or_404(Ticket, id=ticket_id)
        form_ticket = TicketForm(instance=to_answer)
        form_review = ReviewForm()

    elif request.method == 'POST':
        form_ticket = TicketForm(request.POST, request.FILES)
        form_review = ReviewForm(request.POST)
        if validate_form(form_ticket, request):
            validate_form(form_review, request, Ticket.objects.get(title=request.POST["title"],
                                                                   user_id=request.user).id)
        return redirect(index)

    else:
        form_ticket = TicketForm()
        form_review = ReviewForm()

    context = {'title':       title_html,
               'form_review': form_review,
               'form_ticket': form_ticket
               }
    return render(request, 'review/review.html', context)


def register(request):
    """
    Fonction qui permet de s'inscrire sur le site de critique
    :param request:
    :return: Informations à afficher dans le template review.html
    """
    if request.method == 'POST':
        form = Register(request.POST)

        if not form.errors:
            if validate_form(form, request):
                user_name = form.cleaned_data.get('username')
                messages.success(request, "L'utilisateur " + user_name + ' a été enregistré')
                return redirect('login')

    else:
        form = Register()

    context = {
            'title': " - Inscription",
            'form':  form
    }
    return render(request, 'review/register.html', context)


@login_required
def followers(request, delete_id=None):
    """
    Fonction qui gere la page d'abonnement.
    :param request:
    :param delete_id: si fourni, supprime le fait de suivre un utilisateur défini selon l'id de la table User.
    :return: retourne le template follow avec les données à afficher.
    """
    if request.method == 'GET' and delete_id is not None:
        obj = get_object_or_404(UserFollows.objects.filter(user_id=request.user.id,
                                                           followed_user_id=delete_id))
        obj.delete()
        return redirect('abonnement')
    elif request.method == 'POST':
        form = FollowerForm(request.POST)
        validate_form(form, request)
        return redirect('abonnement')
    else:
        followed = UserFollows.objects.filter(user_id=request.user.id)
        followers = UserFollows.objects.filter(followed_user_id=request.user.id)
        form = FollowerForm()

    context = {'title':     ' - Gestion des abonnements',
               'form':      form,
               'followed':  followed,
               'followers': followers
               }

    return render(request, 'review/follow.html', context)
