from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from Aplicaciones.pedidos.models import Pedido
from Aplicaciones.pedidoproductos.models import PedidoProducto
from Aplicaciones.pagos.models import Pago
from Aplicaciones.productos.models import Producto

# Create your views here.


@login_required
def pago_paypal_simulado(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id, usuario=request.user)
    pago = pedido.pago

    if request.method == 'POST':
        pago.estado_pago = 'completado'
        pago.fecha_pago = timezone.now()
        pago.save()

        pedido.estado_pedido = 'enviado'  # o pendiente de envío
        pedido.save()

        return redirect('pedido_confirmado', pedido_id=pedido.id)

    return render(request, 'pagos/paypal_simulado.html', {
        'pedido': pedido,
        'pago': pago
    })

import json
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from Aplicaciones.carrito.models import Carrito
from Aplicaciones.carritoproductos.models import CarritoProducto
from Aplicaciones.productos.models import Producto
from Aplicaciones.pedidos.models import Pedido
from Aplicaciones.pedidoproductos.models import PedidoProducto
from Aplicaciones.pagos.models import Pago


@csrf_exempt
def capture_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            usuario_id = request.session.get('usuario_id')
            metodo_pago = data.get('metodo_pago', 'paypal')  # Captura del frontend

            if not usuario_id:
                return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

            carrito = Carrito.objects.filter(usuario_id=usuario_id, estado='activo').first()
            if not carrito:
                return JsonResponse({'error': 'No hay carrito activo'}, status=404)

            productos_en_carrito = CarritoProducto.objects.filter(carrito=carrito).select_related('producto')
            if not productos_en_carrito.exists():
                return JsonResponse({'error': 'Carrito vacío'}, status=400)

            total = sum(item.cantidad * item.precio_unitario for item in productos_en_carrito)

            # Crear Pedido
            pedido = Pedido.objects.create(
                usuario_id=usuario_id,
                fecha_pedido=timezone.now(),
                total=total,
                estado_pedido='pendiente',
                direccion_envio=carrito.usuario.direccion or 'Dirección no registrada'
            )

            # Agregar productos al pedido y actualizar stock
            for item in productos_en_carrito:
                producto = item.producto
                producto.stock = max(producto.stock - item.cantidad, 0)
                producto.save()

                PedidoProducto.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.precio_unitario
                )

            # Cambiar estado del carrito a pagado
            carrito.estado = 'pagado'
            carrito.save()
            productos_en_carrito.delete()

            # Vaciar carrito en sesión
            if 'carrito' in request.session:
                del request.session['carrito']

            # ✅ Registrar el pago
            Pago.objects.create(
                pedido=pedido,
                monto=total,
                metodo_pago=metodo_pago,
                estado_pago='completado'  # asumes éxito si llega a esta parte
            )

            return JsonResponse({'status': 'success', 'pedido_id': pedido.id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


def gracias(request):
    return render(request, 'pedidos/gracias.html')






