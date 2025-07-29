from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/detalle-pedido/<int:pedido_id>/', views.detalle_pedido_ajax, name='detalle_pedido_ajax'),




]