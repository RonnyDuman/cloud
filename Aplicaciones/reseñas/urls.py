from django.urls import path
from . import views

urlpatterns = [

    path('producto/<int:producto_id>/reseña/', views.agregar_reseña, name='agregar_reseña'),

]
