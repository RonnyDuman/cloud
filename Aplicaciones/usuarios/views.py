from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import Usuario
import uuid
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import random
from django.shortcuts import render
from Aplicaciones.pagos.models import Pago
from Aplicaciones.pedidos.models import Pedido
from django.http import JsonResponse
from Aplicaciones.pedidoproductos.models import PedidoProducto


def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreUsuario')
        correo = request.POST.get('correoUsuario')
        password = request.POST.get('passwordUsuario')

        if not correo.endswith('@gmail.com'):
            messages.error(request, 'Por favor utiliza un correo válido de Gmail.')
            return render(request, 'iniciarSesion/login.html', {'show_register': True})

        verification_code = random.randint(100000, 999999)
        
        send_mail(
            'Código de Verificación',
            f'Tu código de verificación es: {verification_code}',
            settings.DEFAULT_FROM_EMAIL,
            [correo],
            fail_silently=False,
        )
        
        request.session['verification_code'] = verification_code
        request.session['correo'] = correo
        request.session['password'] = password
        request.session['nombre'] = nombre
        
        messages.success(request, 'Se ha enviado un código de verificación a tu correo electrónico.')
        return redirect('verify_email')
    return render(request, 'iniciarSesion/login.html', {'show_register': True})



def perfil_usuario(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    pagos = Pago.objects.filter(pedido__usuario_id=usuario_id).select_related('pedido')

    return render(request, 'usuarios/perfil.html', {
        'pagos': pagos,
    })




def detalle_pedido_ajax(request, pedido_id):
    usuario_id = request.session.get('usuario_id')
    print("Usuario en sesión:", request.session.get('usuario_id'))


    try:
        pedido = Pedido.objects.get(id=pedido_id, usuario_id=usuario_id)
        detalles = PedidoProducto.objects.filter(pedido=pedido).select_related('producto')

        productos = [{
            'nombre': d.producto.nombre,
            'precio_unitario': float(d.precio_unitario),
            'imagen': d.producto.imagen.url if d.producto.imagen else 'https://via.placeholder.com/80x80?text=Sin+imagen'
        } for d in detalles]

        return JsonResponse({'status': 'ok', 'productos': productos})

    except Pedido.DoesNotExist:
        return JsonResponse({'status': 'error', 'error': 'Pedido no encontrado'}, status=404)
