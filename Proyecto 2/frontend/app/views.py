from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Llamada a la API de Flask
        response = requests.post('http://localhost:5000/login', 
            json={'username': username, 'password': password})
        
        if response.status_code == 200:
            data = response.json()
            if data['role'] == 'admin':
                return redirect('CargarUsuarios')
            else:
                return redirect('Galeria')
        else:
            return render(request, 'index.html', {'error': 'Credenciales inválidas'})
            
    return render(request, 'index.html')

def CargarUsuarios(request):
    return render(request, 'CargarUsuarios.html')

def Galeria(request):
    return render(request, 'Galeria.html')

def VerUsuarios(request):
    try:
        response = requests.get('http://localhost:5000/api/get-users')  # Actualizada la URL
        print(f"API Response Status: {response.status_code}")  # Debug
        print(f"API Response Content: {response.text}")  # Debug
        
        if response.status_code == 200:
            data = response.json()
            return render(request, 'VerUsuarios.html', {'users': data.get('users', [])})
        else:
            return render(request, 'VerUsuarios.html', {'error': f'Error al cargar usuarios: {response.text}'})
    except Exception as e:
        print(f"Error in VerUsuarios: {e}")  # Debug
        return render(request, 'VerUsuarios.html', {'error': str(e)})

def VerXML(request):
    return render(request, 'VerXML.html')