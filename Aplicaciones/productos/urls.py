from django.urls import path
from . import views

urlpatterns = [
    path('nuevo/', views.nuevo_producto, name='nuevo_producto'),


    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('productoEd/<int:producto_id>/', views.detalle_productoEd, name='detalle_productoEd'),
    path('producto/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),



]
