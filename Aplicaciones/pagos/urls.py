from django.urls import path
from . import views

urlpatterns = [

    path('capture-order/', views.capture_order, name='capture_order'),
    path('gracias/', views.gracias, name='gracias'),




    

]
