from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

class Usuarios (models.Model):
	nombre = models.CharField (max_length=100)
	correo_electronico = models.CharField (max_length=300)
	password = models.CharField (max_length=30)
	rol = models.CharField (max_length=30)
	
	def __unicode__(self):
		return self.nombre

class Pedidos (models.Model):
	usuario = models.ForeignKey (Usuarios)
	num_pedido = models.CharField (max_length=15)
	concepto = models.CharField(max_length=200)
	estado = models.CharField (max_length=20)
	telefono_tecnico = models.CharField (max_length=12)
	fecha_instalacion = models.DateTimeField ('Fecha de Instalacion')
	forma_de_recepcion = models.CharField (max_length=30)
	
	def __unicode__(self):
		return self.num_pedido

