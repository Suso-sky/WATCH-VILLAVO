from django.urls import path
from .views import RoboListCreateView, RoboDetailView, UsuarioListView

urlpatterns = [
    path('robos/', RoboListCreateView.as_view(), name='robo-list-create'),
    path('robos/<int:pk>/', RoboDetailView.as_view(), name='robo-detail'),
    path('usuarios/', UsuarioListView.as_view(), name='usuario-list'),
]
