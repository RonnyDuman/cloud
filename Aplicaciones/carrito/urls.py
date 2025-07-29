from django.urls import path
from . import views


urlpatterns = [

    path('agregar-carrito/<int:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    
    path('carrito/', views.detalle_carrito, name='detalle_carrito'),
    path('carrito/eliminar/<str:id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('eliminar-del-carrito-db/<int:item_id>/', views.eliminar_del_carrito_db, name='eliminar_del_carrito_db'),

    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),



]
