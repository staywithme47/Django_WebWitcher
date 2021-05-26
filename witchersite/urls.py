from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('about', views.about, name='about'),
    path('project', views.project, name='project'),
    path('welcome', views.welcome, name='welcome'),
    path('game', views.game, name='game'),
    path('user_action', views.user_action, name='user_action'),
    path('endgame', views.end_game, name='endgame'),
]
