from django.db import models
from Aplicaciones.pedidos.models import Pedido
from Aplicaciones.productos.models import Producto
from django.db.models import PROTECT


class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=PROTECT, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre} (Pedido #{self.pedido.id})'
