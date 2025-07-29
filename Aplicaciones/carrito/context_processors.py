from django.db.models import Sum
from Aplicaciones.carritoproductos.models import CarritoProducto
from Aplicaciones.carrito.models import Carrito

def carrito_context(request):
    carrito = request.session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())
    return {'total_items_carrito': total_items}





def carrito_total_items(request):
    usuario_id = request.session.get('usuario_id')
    total_items = 0

    if usuario_id:
        carrito = Carrito.objects.filter(usuario_id=usuario_id, estado='activo').first()
        if carrito:
            total_items = CarritoProducto.objects.filter(carrito=carrito).aggregate(
                total=Sum('cantidad')
            )['total'] or 0
    else:
        carrito_sesion = request.session.get('carrito', {})
        total_items = sum(item['cantidad'] for item in carrito_sesion.values())

    return {'total_items_carrito': total_items}