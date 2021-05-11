"""models.py"""
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class UserModel(models.Model):
    """
    Définition d'un objet abstrait pour définir un héritage par la suite.
    Evite la répétition car le champ user est présent dans plusieurs modèle/classe.
    """
    user = models.ForeignKey(
            to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TimeStampModel(UserModel):
    """
    Définition d'un objet abstrait pour définir un héritage par la suite.
    Evite la répétition car le champ time_created est présent dans plusieurs modèle/classe.
    """
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Ticket(TimeStampModel):
    """
    Définition de l'objet Ticket (Ticket)
    """
    title = models.CharField('Titre', max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return "{} by {}".format(self.title, self.user)


class Review(TimeStampModel):
    """
    Définition de l'objet Critique (Review)
    """
    ticket = models.ForeignKey(to=Ticket, related_name='ticket', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    # valide que la note doit être comprise entre 0 et 5
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)

    def __str__(self):
        return "{} - {}".format(self.ticket.title, self.headline)


class UserFollows(UserModel):
    """
    Définition de l'objet permettant le suivi des utilisateurs (abonnement).
    """
    followed_user = models.ForeignKey(
            to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
            related_name='followed_by')

    class Meta:
        # s'assure que nous n'obtenons pas de multiples instances UserFollows
        # pour les paires uniques utilisateur-utilisateur_followed
        unique_together = ('user', 'followed_user',)

    def __str__(self):
        return "{} suit {}".format(self.user, self.followed_user)
