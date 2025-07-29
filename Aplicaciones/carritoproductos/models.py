from django.db import models
from Aplicaciones.carrito.models import Carrito
from Aplicaciones.productos.models import Producto
from django.db.models import PROTECT


class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=PROTECT, related_name='productos_en_carrito')
    producto = models.ForeignKey(Producto, on_delete=PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre} (Carrito #{self.carrito.id})'

    def subtotal(self):
        return self.cantidad * self.precio_unitario