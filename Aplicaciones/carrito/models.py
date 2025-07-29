from django.db import models
from Aplicaciones.usuarios.models import Usuario
from django.db.models import PROTECT



class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=PROTECT, related_name='carritos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado')
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')

    def __str__(self):
        return f'Carrito #{self.id} - {self.usuario.nombre}'

