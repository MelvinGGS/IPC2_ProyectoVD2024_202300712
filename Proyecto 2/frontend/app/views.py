from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import os
import xml.etree.ElementTree as ET

SESSIONS_FILE = 'session_data.xml'

def save_session(request, role):
    root = ET.Element("session")
    role_elem = ET.SubElement(root, "role")
    role_elem.text = role
    
    tree = ET.ElementTree(root)
    tree.write(SESSIONS_FILE, encoding='utf-8', xml_declaration=True)

def get_session():
    if os.path.exists(SESSIONS_FILE):
        try:
            tree = ET.parse(SESSIONS_FILE)
            root = tree.getroot()
            return root.find('role').text
        except:
            return None
    return None

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        response = requests.post('http://localhost:5000/login', 
            json={'username': username, 'password': password})
        
        if response.status_code == 200:
            data = response.json()
            if data['role'] == 'admin':
                return redirect('CargarUsuarios')
            else:
                return redirect('Galeria')
                
        messages.error(request, 'Credenciales inválidas')
    return render(request, 'index.html')

def CargarUsuarios(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            messages.error(request, 'No se seleccionó ningún archivo')
            return render(request, 'CargarUsuarios.html')
            
        file = request.FILES['file']
        if not file.name:
            messages.error(request, 'El archivo está vacío')
            return render(request, 'CargarUsuarios.html')
            
        files = {'file': (file.name, file, 'text/xml')}
        try:
            response = requests.post('http://localhost:5000/upload', files=files)
            
            if response.status_code == 200:
                messages.success(request, 'Archivo cargado exitosamente')
                xml_content = response.json().get('content', '')
                return render(request, 'CargarUsuarios.html', {'xml_content': xml_content})
            else:
                error_msg = response.json().get('message', 'Error desconocido al cargar el archivo')
                messages.error(request, error_msg)
        except requests.exceptions.RequestException as e:
            messages.error(request, f'Error de conexión: {str(e)}')
    
    # Get XML content for display
    response = requests.get('http://localhost:5000/view-xml')
    xml_content = ''
    if response.status_code == 200:
        xml_content = response.json().get('content', '')
    
    return render(request, 'CargarUsuarios.html', {'xml_content': xml_content})

def Galeria(request):
    return render(request, 'Galeria.html')

def CargarImagen(request):
    return render(request, 'CargarImagen.html')

def EditarImagen(request):
    return render(request, 'EditarImagen.html')

def Ayuda(request):
    return render(request, 'Ayuda.html')

def VerUsuarios(request):
    response = requests.get('http://localhost:5000/api/get-users')
    users = []
    if response.status_code == 200:
        users = response.json().get('users', [])
    return render(request, 'VerUsuarios.html', {'users': users})

def VerXML(request):
    response = requests.get('http://localhost:5000/view-xml')
    content = 'No hay archivo XML cargado'
    if response.status_code == 200:
        content = response.json().get('content', '')
    return render(request, 'VerXML.html', {'content': content})

def logout(request):
    if os.path.exists(SESSIONS_FILE):
        os.remove(SESSIONS_FILE)
    return redirect('index')
