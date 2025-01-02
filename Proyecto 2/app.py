from flask import Flask, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
import os
import re
import time

app = Flask(__name__)

UPLOADED_XML = 'usuarios_cargados.xml'
SESSIONS_XML = 'sessions.xml'

def init_sessions_xml():
    if not os.path.exists(SESSIONS_XML):
        root = ET.Element("sessions")
        tree = ET.ElementTree(root)
        tree.write(SESSIONS_XML, encoding='utf-8', xml_declaration=True)

def create_session(user_id, role):
    init_sessions_xml()
    tree = ET.parse(SESSIONS_XML)
    root = tree.getroot()
    
    # Clean old sessions
    for session in root.findall('session'):
        timestamp = float(session.get('timestamp', 0))
        if time.time() - timestamp > 3600:  # 1 hour expiration
            root.remove(session)
    
    session = ET.SubElement(root, "session")
    session.set('user_id', user_id)
    session.set('role', role)
    session.set('timestamp', str(time.time()))
    
    tree.write(SESSIONS_XML, encoding='utf-8', xml_declaration=True)
    return True

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
                if not validar_id(solicitante.get('id')):
                    continue
                if solicitante.get('id') == username and solicitante.get('pwd') == password:
                    if verificar_solicitante(solicitante):
                        return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        print(f"Intento de login - Usuario: {username}")

        if username == "AdminIPC" and password == "ARTIPC2":
            return jsonify({"status": "success", "role": "admin"})
        
        if not os.path.exists(UPLOADED_XML):
            return jsonify({"status": "error", "message": "No hay usuarios registrados"}), 401
        
        tree = ET.parse(UPLOADED_XML)
        root = tree.getroot()
        
        for solicitante in root.findall('solicitante'):
            if solicitante.get('id') == username and solicitante.get('pwd') == password:
                return jsonify({"status": "success", "role": "user"})
        
        return jsonify({"status": "error", "message": "Credenciales inválidas"}), 401
    except Exception as e:
        print(f"Error en login: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            print("No file part in request")
            return jsonify({
                "status": "error", 
                "message": "No se seleccionó ningún archivo"
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            print("Empty filename")
            return jsonify({
                "status": "error", 
                "message": "Nombre de archivo vacío"
            }), 400
            
        if not file.filename.endswith('.xml'):
            print("Invalid file type")
            return jsonify({
                "status": "error", 
                "message": "El archivo debe ser XML"
            }), 400

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
        
        new_root = ET.Element("solicitantes")
        for user in valid_users:
            new_root.append(user)
        
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
        print(f"Upload error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error al procesar archivo: {str(e)}"
        }), 500

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

@app.route('/api/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():
    if request.method == 'GET':
        try:
            response = get_users()
            return response
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not validar_id(data.get('id')):
                return jsonify({"status": "error", "message": "ID inválido"}), 400
            # Add more validation...
            return jsonify({"status": "success", "message": "Usuario creado"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    elif request.method == 'PUT':
        data = request.get_json()
        # Add user update logic
        return jsonify({"status": "success", "message": "User updated"})

    elif request.method == 'DELETE':
        user_id = request.args.get('id')
        # Add user deletion logic
        return jsonify({"status": "success", "message": "User deleted"})

@app.route('/api/xml', methods=['GET', 'POST'])
def xml_operations():
    if request.method == 'GET':
        try:
            if os.path.exists(UPLOADED_XML):
                tree = ET.parse(UPLOADED_XML)
                root = tree.getroot()
                content = ET.tostring(root, encoding='unicode', method='xml')
                return jsonify({"status": "success", "content": content})
            return jsonify({"status": "error", "message": "No XML file found"}), 404
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    elif request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file part"}), 400
        # ... existing XML upload logic ...

@app.route('/api/xml/users', methods=['GET'])
def view_users_xml():
    try:
        if os.path.exists(UPLOADED_XML):
            with open(UPLOADED_XML, 'r', encoding='utf-8') as file:
                content = file.read()
            return jsonify({"status": "success", "content": content})
        return jsonify({"status": "error", "message": "Archivo no encontrado"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)