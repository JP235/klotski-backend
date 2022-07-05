from django.urls import path, include
from .views import *
from knox.views import LogoutView

urlpatterns = [  
    path('boards/', GameKlotskiList.as_view(), name='game_list'),
    path('openboards/', GameKlotskiListOpen.as_view(), name='open_game_list'),
    path('game/<str:game_code>/', GameView.as_view(), name='game'),
  
    path('auth/register', RegisterAPIView.as_view()),
    path('auth/user', UserAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
    path('auth/logout/', LogoutView.as_view(), name='knox_logout')
]