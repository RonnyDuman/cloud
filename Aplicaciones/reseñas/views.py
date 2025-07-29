from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from Aplicaciones.productos.models import Producto
from Aplicaciones.reseñas.models import Reseña
from Aplicaciones.usuarios.models import Usuario
from django.contrib import messages

def agregar_reseña(request, producto_id):
    if not request.session.get('usuario_id'):
        messages.error(request, "Debes iniciar sesión para dejar una reseña.")
        return redirect('login')

    if request.method == 'POST':
        usuario = Usuario.objects.get(id=request.session['usuario_id'])
        producto = get_object_or_404(Producto, id=producto_id)
        calificacion = int(request.POST.get('calificacion'))
        comentario = request.POST.get('comentario', '').strip()

        # Guardar o actualizar reseña (opcional: 1 reseña por usuario por producto)
        reseña, created = Reseña.objects.update_or_create(
            usuario=usuario,
            producto=producto,
            defaults={'calificacion': calificacion, 'comentario': comentario}
        )

        messages.success(request, "Gracias por tu reseña.")
        return redirect('detalle_producto', producto_id=producto_id)

    return redirect('detalle_producto', producto_id=producto_id)
