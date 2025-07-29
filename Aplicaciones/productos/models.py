from django.db import models
from Aplicaciones.categorias.models import Categoria
from django.db.models import PROTECT


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.FileField(upload_to='productos/', blank=True, null=True)  # CAMBIO
    categoria = models.ForeignKey(Categoria, on_delete=PROTECT, related_name='productos')

    def __str__(self):
        return self.nombre
