from rest_framework import generics
from .models import Robo, Usuario
from .serializers import RoboSerializer, UsuarioSerializer

class RoboListCreateView(generics.ListCreateAPIView):
    queryset = Robo.objects.all()
    serializer_class = RoboSerializer

class RoboDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Robo.objects.all()
    serializer_class = RoboSerializer

class UsuarioListView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
