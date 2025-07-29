from django.db import models
from Aplicaciones.pedidos.models import Pedido
from django.db.models import PROTECT


class Pago(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=PROTECT, related_name='pago')
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50, choices=[
        ('tarjeta', 'Tarjeta'),
        ('paypal', 'PayPal'),
        ('transferencia', 'Transferencia Bancaria'),
        ('criptomoneda', 'Criptomoneda'),
    ])
    estado_pago = models.CharField(max_length=20, choices=[
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
        ('pendiente', 'Pendiente'),
    ])

    def __str__(self):
        return f'Pago de Pedido #{self.pedido.id} - {self.estado_pago}'
