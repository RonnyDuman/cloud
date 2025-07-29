import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.db.models import ProtectedError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.decorators.http import require_http_methods
from Aplicaciones.categorias.models import Categoria




@csrf_exempt 
def categoria_list_create(request):
    if request.method == 'GET':
        categorias = list(Categoria.objects.values('id', 'nombre'))
        return JsonResponse(categorias, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            if not nombre:
                return JsonResponse({'error': 'El campo nombre es obligatorio.'}, status=400)
            categoria = Categoria.objects.create(nombre=nombre)
            return JsonResponse({'id': categoria.id, 'nombre': categoria.nombre}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])



@csrf_exempt
def categoria_detail(request, id):
    try:
        categoria = Categoria.objects.get(id=id)
    except Categoria.DoesNotExist:
        return JsonResponse({'error': 'Categoría no encontrada'}, status=404)
    
    if request.method == 'GET':
        return JsonResponse({'id': categoria.id, 'nombre': categoria.nombre})
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
            nombre = data.get('nombre')
            if not nombre:
                return JsonResponse({'error': 'El campo nombre es obligatorio.'}, status=400)
            
            categoria.nombre = nombre
            categoria.save()
            return JsonResponse({'id': categoria.id, 'nombre': categoria.nombre})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        try:
            categoria.delete()
            return JsonResponse({'message': 'Categoría eliminada correctamente'})
        except ProtectedError:
            return JsonResponse({'error': 'No se puede eliminar la categoría porque tiene productos asociados'}, status=400)

    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])





@require_http_methods(["DELETE"])
def categoria_eliminar(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    try:
        categoria.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'No se puede eliminar: categoría usada en productos.'}, status=400)
