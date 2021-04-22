from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('ticket/', views.ticket, name='ticket'),
    path('ticket/<int:ticket_id>/', views.ticket),
    path('review/', views.review, name='review'),
    path('review/<int:review_id>/', views.review),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
