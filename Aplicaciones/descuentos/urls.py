from django.urls import path
from . import views
urlpatterns = [

    path('nuevo/', views.nuevo_descuento, name='nuevo_descuento'),
    path('descuentos/editar/<int:descuento_id>/', views.editar_descuento, name='editar_descuento'),



]
