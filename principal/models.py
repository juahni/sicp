from django.db import models
# Importamos la tabla User.
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    """
    Esta clase extiene el modelo User de django para agragarle
    los campos que se necesitan en la base de datos.

    """

    # Campos agregados al modelo User.
    ci = models.IntegerField(unique=True, null=True)
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    # Clave foranea unica al modelo User. Establece la relacion uno a uno.
    user = models.ForeignKey(User, unique=True)