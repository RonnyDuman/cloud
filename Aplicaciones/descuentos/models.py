from django.db import models
from Aplicaciones.productos.models import Producto
from django.db.models import PROTECT


class Descuento(models.Model):
    producto = models.ForeignKey(Producto, on_delete=PROTECT, related_name='descuentos')
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f'{self.porcentaje_descuento}% off - {self.producto.nombre}'
