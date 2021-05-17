# __P9 Projet LITReview__

## Etat d'avancement :

~~En dev -~~ **Prêt pour la soutenance**

## Description :

>Ceci est une application Web permettant un des utilisateurs inscrits d'emettre des demandes de critiques de livres
    ou d'articles et d'y repondre.

Il y a plusieurs mode de fonctionnement : 
* Un utilisateur demande une critique d'un livre particulier.
  * Si celui-ci (l'utilisateur) est suivi, un de ses abonnés peut émettre une critique.
* Un utilisateur suit un autre et voit qu'une demande de critique est émise, il peut y répondre.
* Un utilisateur souhaite émettre une critique sur un article/livre, il peut le faire en émettant un ticket en 
meme temps.


>Les auteurs (utilisateurs) sont toujours 'responsable' de leurs publications. Elles ne peuvent être supprimés ou 
    édités par personnes d'autres (exception faites des superusers).


## Installation
Se diriger sur le repertoire où l'on souhaite installer l'environnement virtuel.
1. Cloner le repository via la commande : 
`git clone https://github.com/Manu512/P9_LITReview.git`

  
2. Création de l'environnement virtuel

Exécuter la commande :
* `python3 -m venv 'env'` ('env' sera le repertoire où seront stocké les données de l'environnement python)
  
3. Activation et installations des dépendances nécessaires au script dans l'environnement virtuel   
   `env/Script/activate`
   
   `pip install -r requirements.txt'`


4. Lancement du serveur Django : 

* `python manage.py runserver`

A ce moment, page sera accessible à l'URL [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Utilisation

1. Suivre l'url [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
2. S'inscrire
3. S'authentifier
4. Créer un ticket ou une critique.
5. Suivre un utilisateur existant (par exemple : emmanuel, estelle ou jean8597)

### Listes des utilisateurs de test :

emmanuel
estelle
bernard
jean8597
sarahj
arnaud
severine123
raphael
eliane

> Le mot de passe est : test

>Il va de soit que cela n'est pas sécurisé mais lors de la création manuelle d'utilisateur, des restrictions sont en 
> places. Voir setting.py de la configuration Django

