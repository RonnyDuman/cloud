from django.shortcuts import render, redirect, get_object_or_404
from Aplicaciones.productos.models import Producto
from Aplicaciones.categorias.models import Categoria
from Aplicaciones.carrito.models import Carrito
from decimal import Decimal
from Aplicaciones.carritoproductos.models import CarritoProducto
from django.contrib import messages
from Aplicaciones.usuarios.models import Usuario
from decimal import Decimal
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
import uuid
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import random
from Aplicaciones.descuentos.models import Descuento
from Aplicaciones.core.decorators import admin_required


# Create your views here.




def General(request):
    productos = Producto.objects.all()
    descuentos = {d.producto_id: d for d in Descuento.objects.all()} 

    carrito = request.session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())

    return render(request, 'Inicio/inicio.html', {
        'productos': productos,
        'descuentos': descuentos,
        'total_items': total_items,
    })


def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    descuentos = {d.producto_id: d for d in Descuento.objects.all()}

    carrito = request.session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())

    return render(request, 'Inicio/categoria.html', {
        'categoria': categoria,
        'productos': productos,
        'descuentos': descuentos,
        'total_items': total_items,
    })




def productos_con_descuento(request):
    descuentos = Descuento.objects.select_related('producto').all()
    productos = [d.producto for d in descuentos]

    descuentos_dict = {d.producto_id: d for d in descuentos}

    carrito = request.session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())

    return render(request, 'Inicio/descuentos.html', {
        'productos': productos,
        'descuentos': descuentos_dict,
        'total_items': total_items,
    })

def todos_productos(request):
    productos = Producto.objects.all()
    descuentos = {d.producto_id: d for d in Descuento.objects.all()}

    carrito = request.session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())

    return render(request, 'Inicio/todos.html', {
        'productos': productos,
        'descuentos': descuentos,
        'total_items': total_items,
        'mostrar_carousel': False,  
    })



def sesionInicada(request):
    correo = request.POST.get('correoUsuario')
    password = request.POST.get('passwordUsuario')

    if correo == 'admin1234' and password == '1234admin':
        request.session['admin_token'] = True
        return redirect('admin_inicio')

    try:
        usuario = Usuario.objects.get(email=correo)
        if check_password(password, usuario.contraseña):
            request.session['usuario_id'] = usuario.id

            carrito_sesion = request.session.get('carrito', {})
            carrito_db, created = Carrito.objects.get_or_create(usuario=usuario, estado='activo')

            for prod_id, item in carrito_sesion.items():
                producto = Producto.objects.get(id=prod_id)

                precio_final = Decimal(item.get('precio_descuento', item['precio']))

                item_db, creado = CarritoProducto.objects.get_or_create(
                    carrito=carrito_db,
                    producto=producto,
                    defaults={
                        'cantidad': item['cantidad'],
                        'precio_unitario': precio_final
                    }
                )
                if not creado:
                    item_db.cantidad += item['cantidad']
                    item_db.save()

            request.session['carrito'] = {}

            return redirect('General')

        else:
            messages.error(request, 'Contraseña incorrecta')

    except Usuario.DoesNotExist:
        messages.error(request, 'Correo no registrado')

    return redirect('login')


def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        contraseña = request.POST.get('contraseña')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')

        if not email.endswith('@gmail.com'):
            messages.error(request, 'Solo se permiten correos @gmail.com')
            return render(request, 'usuarios/login.html', {'show_register': True})

        verification_code = random.randint(100000, 999999)

        send_mail(
            'Código de Verificación',
            f'Tu código de verificación es: {verification_code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        # Guardar todos los datos en sesión para usarlos luego
        request.session['verification_code'] = verification_code
        request.session['email'] = email
        request.session['contraseña'] = contraseña
        request.session['nombre'] = nombre
        request.session['telefono'] = telefono
        request.session['direccion'] = direccion

        messages.success(request, 'Se ha enviado un código de verificación a tu correo electrónico.')
        return redirect('verify_email')

    return render(request, 'usuarios/login.html', {'show_register': True})




def verify_email(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        if verification_code == str(request.session.get('verification_code')):
            email = request.session.get('email')
            contraseña = request.session.get('contraseña')
            nombre = request.session.get('nombre')
            telefono = request.session.get('telefono')
            direccion = request.session.get('direccion')

            if not Usuario.objects.filter(email=email).exists():
                usuario = Usuario(
                    nombre=nombre,
                    email=email,
                    contraseña=make_password(contraseña),
                    telefono=telefono,
                    direccion=direccion
                )
                usuario.save()
                messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            else:
                messages.info(request, 'El usuario ya existe. Inicia sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Código de verificación incorrecto. Intenta de nuevo.')
    return render(request, 'usuarios/verify.html')




def IniciarSesion(request):
    if request.method == 'POST':
        correo = request.POST['correoUsuario']  
        clave = request.POST['passwordUsuario']

        if correo == 'admin1234' and clave == '1234admin':
            print("comprobando si entro a este bloque")
            request.session['admin_token'] = True
            return redirect('admin_inicio')

        try:
            usuario = Usuario.objects.get(email=correo, contraseña=clave)
            print(usuario)
            print("clave ", clave)
            request.session['usuario_id'] = usuario.id
            return redirect('realizar_compra')
        except Usuario.DoesNotExist:
            messages.error(request, "Correo o contraseña incorrectos.")

    return render(request, 'usuarios/login.html')









def cerrar_sesion(request):
    request.session.flush()
    return redirect('General')










#######VISTAS DEL ADMINISTRADOR###





@admin_required
def inicio_admin(request):
    return render(request, 'admin/inicio.html')



@admin_required
def admin_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos})



@admin_required
def admin_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/lista.html', {'categorias': categorias})




def admin_descuentos(request):
    descuentos = Descuento.objects.select_related('producto').all()
    return render(request, 'descuentos/lista.html', {'descuentos': descuentos})
