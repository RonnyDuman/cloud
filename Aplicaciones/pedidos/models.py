from django.db import models
from Aplicaciones.usuarios.models import Usuario
from django.db.models import PROTECT


class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=PROTECT, related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pedido = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ], default='pendiente')
    direccion_envio = models.TextField()

    def __str__(self):
        return f'Pedido #{self.id} - {self.usuario.nombre}'
