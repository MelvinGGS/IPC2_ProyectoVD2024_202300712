from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('CargarUsuarios/', views.CargarUsuarios, name='CargarUsuarios'),
    path('Galeria/', views.Galeria, name='Galeria'),
    path('VerUsuarios/', views.VerUsuarios, name='VerUsuarios'),
    path('VerXML/', views.VerXML, name='VerXML'),
    path('CargarImagen/', views.CargarImagen, name='CargarImagen'),
    path('EditarImagen/', views.EditarImagen, name='EditarImagen'),
    path('Ayuda/', views.Ayuda, name='Ayuda'),
]