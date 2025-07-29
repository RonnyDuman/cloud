from django.urls import path
from . import views

urlpatterns = [

    path('realizar-compra/', views.realizar_compra, name='realizar_compra'),

]
