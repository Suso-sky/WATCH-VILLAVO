from django.urls import path
from .views import RoboListCreateView, RoboDetailView, UsuarioListView, mapa_calor

urlpatterns = [
    path('robos/', RoboListCreateView.as_view(), name='robo-list-create'),
    path('robos/<int:pk>/', RoboDetailView.as_view(), name='robo-detail'),
    path('usuarios/', UsuarioListView.as_view(), name='usuario-list'),
    path('mapa_calor/', mapa_calor, name='mapa_calor'),
]
