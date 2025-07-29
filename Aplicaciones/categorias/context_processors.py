from Aplicaciones.categorias.models import Categoria

def categorias_disponibles(request):
    categorias = Categoria.objects.all()
    return {'categorias_globales': categorias}
