from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.index, name='post'),
    path('register/', views.register, name='register'),
    path('ticket/', views.ticket, name='ticket'),
    path('ticket/edit/<int:ticket_edit_id>/', views.ticket, name='ticket_edit'),
    path('ticket/delete/<int:ticket_delete_id>/', views.ticket, name='ticket_delete'),
    path('review/', views.review, name='review'),
    path('review/reply/<int:ticket_id>/', views.review, name='reply_ticket'),
    path('review/delete/<int:review_delete_id>/', views.review, name='delete_review'),
    path('review/edit/<int:review_edit_id>/', views.review, name='edit_review'),
    path('login/', views.Login.as_view(), name='login'),
    path('followers/', views.followers, name='abonnement'),
    path('followers/delete/<int:delete_id>/', views.followers, name='abonnement-delete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
