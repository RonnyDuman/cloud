from Aplicaciones.productos.models import Producto
from Aplicaciones.categorias.models import Categoria
import os
from django.conf import settings
from django.db.models import ProtectedError
from django.contrib import messages
from Aplicaciones.productos.models import Producto
from django.shortcuts import render, get_object_or_404, redirect
from Aplicaciones.core.decorators import admin_required
from Aplicaciones.descuentos.models import Descuento
# Create your views here.



def nuevo_producto(request):
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio').replace(",",".")
        stock = request.POST.get('stock')
        categoria_id = request.POST.get('categoria')
        imagen = request.FILES.get('imagen')

        if all([nombre, descripcion, precio, stock, categoria_id]):
            Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                stock=stock,
                imagen=imagen,
                categoria_id=categoria_id
            )
            return redirect('admin_productos')

    return render(request, 'productos/nuevo.html', {'categorias': categorias})









def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    reseñas = producto.reseñas.select_related('usuario').order_by('-fecha')

    # Obtener descuento si existe
    descuento_obj = Descuento.objects.filter(producto=producto).first()
    descuentos = {producto.id: descuento_obj} if descuento_obj else {}

    # Obtener el carrito
    carrito = request.session.get('carrito', {})
    producto_en_carrito = str(producto.id) in carrito  # ← True si ya está agregado

    return render(request, 'productos/detalle.html', {
        'producto': producto,
        'descuentos': descuentos,
        'producto_en_carrito': producto_en_carrito,
        'reseñas': reseñas,
        'rango_estrellas': range(1, 6),
    })




@admin_required
def detalle_productoEd(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST['descripcion']
        producto.precio = request.POST['precio']
        producto.stock = request.POST['stock']
        producto.categoria_id = request.POST['categoria']

        if 'imagen' in request.FILES:
            # Eliminar la imagen anterior si existe
            if producto.imagen and os.path.isfile(producto.imagen.path):
                os.remove(producto.imagen.path)

            # Asignar la nueva imagen
            producto.imagen = request.FILES['imagen']

        producto.save()
        return redirect('admin_productos')

    categorias = Categoria.objects.all()
    return render(request, 'productos/edicion.html', {
        'producto': producto,
        'categorias': categorias
    })



@admin_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    try:
        # Guardar la ruta absoluta de la imagen antes de eliminar el producto
        if producto.imagen:
            ruta_imagen = os.path.join(settings.MEDIA_ROOT, str(producto.imagen.path))
        else:
            ruta_imagen = None

        producto.delete()

        # Si la eliminación fue exitosa, borrar también la imagen del sistema
        if ruta_imagen and os.path.isfile(ruta_imagen):
            os.remove(ruta_imagen)

        messages.success(request, "Producto eliminado correctamente.")
    except ProtectedError:
        messages.error(request, "❌ No se puede eliminar este producto porque está relacionado con otros registros (carritos, pedidos, etc.).")
    except Exception as e:
        messages.error(request, f"⚠️ Error al eliminar la imagen: {e}")

    return redirect('admin_productos')
