from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from Aplicaciones.pedidos.models import Pedido
from Aplicaciones.pedidoproductos.models import PedidoProducto
from Aplicaciones.pagos.models import Pago
from Aplicaciones.productos.models import Producto


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Aplicaciones.carrito.models import Carrito
from Aplicaciones.productos.models import Producto
from Aplicaciones.usuarios.models import Usuario


def realizar_compra(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    # Traer usuario desde sesión manual
    usuario = Usuario.objects.get(id=usuario_id)

    # Luego continúa igual
    carrito_db = Carrito.objects.filter(usuario=usuario, estado='activo').first()


    print(carrito_db)
    if carrito_db:
        # Obtener los productos y cantidades del carrito en BD
        items = carrito_db.productos_en_carrito.select_related('producto').all()

        # Armar un diccionario tipo sesión para reutilizar lógica o templates
        carrito = {}
        for item in items:
            carrito[str(item.producto.id)] = {
                'nombre': item.producto.nombre,
                'precio_descuento': float(item.precio_unitario),  # ajusta si tienes campo descuento
                'cantidad': item.cantidad,
                'total': float(item.subtotal()),
            }
    else:
        # Si no hay carrito en BD, intentar obtener de sesión (para fallback)
        carrito = request.session.get('carrito', {})

    if not carrito:
        # Si sigue vacío, redirigir al detalle carrito o página principal
        return redirect('detalle_carrito')

    # Calcular subtotal y total
    subtotal = sum(item['precio_descuento'] * item['cantidad'] for item in carrito.values())

    context = {
        'carrito': carrito,
        'subtotal': subtotal,
        'total': subtotal,
    }

    return render(request, 'pedidos/realizar.html', context)





def realizar_compra_ejecutar(request):
    usuario = request.user

    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('detalle_carrito')  # o mostrar mensaje

    if request.method == 'POST':
        direccion = request.POST['direccion']
        metodo_pago = request.POST['metodo_pago']

        # Calcular total
        total = sum(item['precio_descuento'] * item['cantidad'] for item in carrito.values())

        # 1. Crear el pedido
        pedido = Pedido.objects.create(
            usuario=usuario,
            total=total,
            direccion_envio=direccion,
            estado_pedido='pendiente'
        )

        # 2. Crear los items
        for item in carrito.values():
            producto = Producto.objects.get(nombre=item['nombre'])  # o por ID si lo guardas en la sesión
            PedidoProducto.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=item['cantidad'],
                precio_unitario=item['precio_descuento']
            )
            # Simular reducción de stock
            producto.stock -= item['cantidad']
            producto.save()

        # 3. Crear el pago pendiente
        Pago.objects.create(
            pedido=pedido,
            monto=total,
            metodo_pago=metodo_pago,
            estado_pago='pendiente'
        )

        # 4. Vaciar carrito
        del request.session['carrito']
        request.session.modified = True

        # 5. Redirigir a "simular pago"
        return redirect('pago_paypal_simulado', pedido_id=pedido.id)

    return render(request, 'pedidos/realizar.html')
