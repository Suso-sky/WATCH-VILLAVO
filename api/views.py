from rest_framework import generics
from .models import Robo, Usuario
from .serializers import RoboSerializer, UsuarioSerializer
from django.shortcuts import render

class RoboListCreateView(generics.ListCreateAPIView):
    queryset = Robo.objects.all()
    serializer_class = RoboSerializer

class RoboDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Robo.objects.all()
    serializer_class = RoboSerializer

class UsuarioListView(generics.ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

def mapa_calor(request):
    return render(request, 'mapa_calor.html')
