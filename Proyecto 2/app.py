from flask import Flask, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
import os
import re

app = Flask(__name__)
CORS(app)

"""
API Endpoints:

1. Login
   POST http://localhost:5000/login
   Body: {
       "username": "AdminIPC",
       "password": "ARTIPC2"
   }

2. Cargar XML
   POST http://localhost:5000/upload
   Body (Form-data):
   - Key: file
   - Value: [archivo XML]

3. Ver XML
   GET http://localhost:5000/view-xml

4. Obtener Usuarios
   GET http://localhost:5000/api/get-users
"""

UPLOADED_XML = 'usuarios_cargados.xml'

# Funciones de validación mejoradas
def validar_id(id_usuario):
    patron = r'^IPC-\d+$'
    if not bool(re.match(patron, id_usuario)):
        print(f"ID inválido (debe ser formato IPC-XXX): {id_usuario}")
        return False
    return True

def validar_correo(correo):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not bool(re.match(patron, correo)):
        print(f"Correo inválido: {correo}")
        return False
    return True

def validar_telefono(telefono):
    if not (telefono.isdigit() and len(telefono) == 8):
        print(f"Teléfono inválido (debe tener 8 dígitos): {telefono}")
        return False
    return True

def verificar_solicitante(solicitante):
    try:
        id_usuario = solicitante.get('id')
        correo = solicitante.find('CorreoElectronico').text
        telefono = solicitante.find('NumeroTelefono').text
        
        if not validar_id(id_usuario):
            print(f"ID inválido: {id_usuario}")
            return False
        if not validar_correo(correo):
            print(f"Correo inválido: {correo}")
            return False
        if not validar_telefono(telefono):
            print(f"Teléfono inválido: {telefono}")
            return False
        return True
    except Exception as e:
        print(f"Error en validación: {e}")
        return False

def verify_user(username, password):
    try:
        if os.path.exists(UPLOADED_XML):
            tree = ET.parse(UPLOADED_XML)
            root = tree.getroot()
            for solicitante in root.findall('solicitante'):
                # Primero validamos el formato del ID
                if not validar_id(solicitante.get('id')):
                    continue
                # Luego verificamos las credenciales
                if solicitante.get('id') == username and solicitante.get('pwd') == password:
                    # Finalmente validamos el resto de datos
                    if verificar_solicitante(solicitante):
                        return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    print(f"Intento de login - Usuario: {username}")  # Debug

    if username == "AdminIPC" and password == "ARTIPC2":
        return jsonify({"status": "success", "role": "admin"})
    
    # Validar formato del ID antes de intentar cualquier autenticación
    if not validar_id(username):
        return jsonify({"status": "error", "message": "ID de usuario inválido"}), 401
    
    if verify_user(username, password):
        return jsonify({"status": "success", "role": "user"})
    
    return jsonify({"status": "error", "message": "Credenciales inválidas"}), 401

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400
    
    if file and file.filename.endswith('.xml'):
        try:
            # Validación y filtrado de usuarios
            temp_path = 'temp_upload.xml'
            file.save(temp_path)
            tree = ET.parse(temp_path)
            root = tree.getroot()
            
            valid_users = []
            ids_vistos = set()
            invalid_count = 0
            
            for solicitante in root.findall('solicitante'):
                try:
                    id_usuario = solicitante.get('id')
                    correo = solicitante.find('CorreoElectronico').text
                    telefono = solicitante.find('NumeroTelefono').text
                    
                    # Validaciones estrictas
                    if not validar_id(id_usuario) or \
                       not validar_correo(correo) or \
                       not validar_telefono(telefono) or \
                       id_usuario in ids_vistos:
                        invalid_count += 1
                        continue
                    
                    ids_vistos.add(id_usuario)
                    valid_users.append(solicitante)
                    
                except Exception as e:
                    print(f"Error procesando usuario: {e}")
                    invalid_count += 1
                    continue
            
            # Crear nuevo XML solo con usuarios válidos
            new_root = ET.Element("solicitantes")
            for user in valid_users:
                new_root.append(user)
            
            # Guardar XML filtrado
            tree = ET.ElementTree(new_root)
            tree.write(UPLOADED_XML, encoding='utf-8', xml_declaration=True)
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            message = f"Archivo cargado. Usuarios válidos: {len(valid_users)}, Usuarios inválidos: {invalid_count}"
            print(message)
            
            return jsonify({
                "status": "success",
                "message": message,
                "content": ET.tostring(new_root, encoding='unicode', method='xml')
            })
            
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return jsonify({"status": "error", "message": str(e)}), 400
    
    return jsonify({"status": "error", "message": "Invalid file type"}), 400

@app.route('/view-xml', methods=['GET'])
def view_xml():
    try:
        if os.path.exists(UPLOADED_XML):
            tree = ET.parse(UPLOADED_XML)
            root = tree.getroot()
            content = ET.tostring(root, encoding='unicode', method='xml')
            return jsonify({
                "status": "success",
                "content": content
            })
        else:
            return jsonify({
                "status": "error",
                "message": "No XML file has been uploaded yet"
            }), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/get-users', methods=['GET'])
def get_users():
    try:
        if not os.path.exists(UPLOADED_XML):
            return jsonify({"status": "error", "message": "No XML file found"}), 404

        tree = ET.parse(UPLOADED_XML)
        root = tree.getroot()
        users = []
        
        for solicitante in root.findall('solicitante'):
            # Ya no necesitamos validar aquí porque el XML ya está filtrado
            user = {
                'id': solicitante.get('id'),
                'nombre': solicitante.find('NombreCompleto').text,
                'correo': solicitante.find('CorreoElectronico').text,
                'telefono': solicitante.find('NumeroTelefono').text,
                'direccion': solicitante.find('Direccion').text,
                'perfil': solicitante.find('perfil').text
            }
            users.append(user)

        return jsonify({
            "status": "success",
            "users": users
        })
    except Exception as e:
        print(f"Error in get_users: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)