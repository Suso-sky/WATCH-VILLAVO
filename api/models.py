from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Categoria(models.TextChoices):
    VEHICULOS = 'Vehículos'
    PEATONES = 'Peatones'
    VIVIENDAS = 'Viviendas'

class Rol(models.TextChoices):
    CIVIL = 'Civil'
    ADMINISTRADOR = 'Administrador'

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, password=None):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")
        user = self.model(email=self.normalize_email(email), nombre=nombre)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, password=None):
        user = self.create_user(email, nombre, password)
        user.rol = Rol.ADMINISTRADOR
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.CIVIL)
    suscripcion = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    objects = UsuarioManager()

    def __str__(self):
        return self.email

class Robo(models.Model):
    categoria = models.CharField(max_length=50, choices=Categoria.choices)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField()
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.categoria} - {self.fecha_hora}"
    
class Tweet(models.Model):
    id = models.BigAutoField(primary_key=True)
    tweet_text = models.TextField()
    created_at = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

class RoboMedellin(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_hecho = models.DateTimeField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    sexo = models.CharField(max_length=10)
    edad = models.IntegerField()
    medio_transporte = models.CharField(max_length=50)
    modalidad = models.CharField(max_length=100)
    nombre_barrio = models.CharField(max_length=100)
    codigo_comuna = models.IntegerField()

    def __str__(self):
        return f"{self.modalidad} en {self.nombre_barrio} ({self.fecha_hecho})"
