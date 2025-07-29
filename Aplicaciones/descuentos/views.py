from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib import messages
from Aplicaciones.productos.models import Producto
from Aplicaciones.descuentos.models import Descuento
from django.utils import timezone

def nuevo_descuento(request):
    productos = Producto.objects.all()
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        porcentaje = request.POST.get('porcentaje_descuento')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        hoy = timezone.now().date()
        descuento_activo = Descuento.objects.filter(
            producto_id=producto_id,
            fecha_inicio__lte=hoy,
            fecha_fin__gte=hoy
        ).first()

        if descuento_activo:
            descuento_activo.porcentaje_descuento = porcentaje
            descuento_activo.fecha_inicio = fecha_inicio
            descuento_activo.fecha_fin = fecha_fin
            descuento_activo.save()
            messages.success(request, 'Descuento actualizado correctamente')
        else:
            Descuento.objects.create(
                producto_id=producto_id,
                porcentaje_descuento=porcentaje,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            messages.success(request, 'Descuento creado correctamente')

        return redirect('admin_descuentos')

    return render(request, 'descuentos/nuevo.html', {'productos': productos})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from Aplicaciones.descuentos.models import Descuento

def editar_descuento(request, descuento_id):
    descuento = get_object_or_404(Descuento, id=descuento_id)

    if request.method == 'POST':
        porcentaje = request.POST.get('porcentaje_descuento')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        descuento.porcentaje_descuento = porcentaje
        descuento.fecha_inicio = fecha_inicio
        descuento.fecha_fin = fecha_fin
        descuento.save()

        messages.success(request, 'Descuento actualizado correctamente')
        return redirect('admin_descuentos')

    # GET
    porcentaje_entero = int(descuento.porcentaje_descuento)
    return render(request, 'descuentos/editar.html', {
        'descuento': descuento,
        'porcentaje_entero': porcentaje_entero,
    })
