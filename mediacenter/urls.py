from django.urls import path

from mediacenter.views import player, controller, Players

urlpatterns = [
    path('player', player, name='player'),
    path('controller/<str:room>', controller, name='controller'),
    path('players', Players.as_view(), name='players'),
]