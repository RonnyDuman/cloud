from django.db import models
from Aplicaciones.usuarios.models import Usuario
from Aplicaciones.productos.models import Producto
from django.db.models import PROTECT


class Reseña(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=PROTECT, related_name='reseñas')
    producto = models.ForeignKey(Producto, on_delete=PROTECT, related_name='reseñas')
    calificacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.nombre} - {self.producto.nombre} ({self.calificacion}★)'
