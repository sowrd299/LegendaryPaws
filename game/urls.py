from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_index, name='game_index'),
    path('action/', views.handle_action, name='handle_action'),
    path('reset/', views.reset_session, name='reset_session'),
]
