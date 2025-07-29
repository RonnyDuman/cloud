from django.urls import path
from . import views

urlpatterns = [


    path('api/categorias/', views.categoria_list_create, name='categoria_list_create'),  # GET lista, POST crea
    path('api/categorias/<int:id>/', views.categoria_detail, name='categoria_detail'),


]
