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

'''
- LOGIN
POST http://localhost:5000/login
Content-Type: application/json

{
    "username": "IPC-123",
    "password": "contraseña123"
}

- VER XML USUARIOS
GET http://localhost:5000/view-xml


- OBTENER USUARIOS
GET http://localhost:5000/api/get-users

- CARGAR USUARIOS
POST http://localhost:5000/upload
'''