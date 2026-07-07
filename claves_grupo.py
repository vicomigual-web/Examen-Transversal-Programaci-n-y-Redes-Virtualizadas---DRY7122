from flask import Flask, request, jsonify
import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)
# Nombre del archivo reflejando a ambos integrantes del grupo
DB_NAME = 'usuarios_comigual_lazcano.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Se mantienen los campos exigidos por la rúbrica
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       usuario TEXT UNIQUE, 
                       password_hash TEXT,
                       fecha_creacion TEXT)''')
    conn.commit()
    conn.close()
    print(f"[*] Base de datos '{DB_NAME}' inicializada correctamente.")
    print("[*] Integrantes: Vicente Comigual y Gabriel Lazcano")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    usuario = data.get('usuario')
    password = data.get('password')

    if not usuario or not password:
        return jsonify({"mensaje": "Faltan parametros"}), 400

    pwd_hash = hash_password(password)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, password_hash, fecha_creacion) VALUES (?, ?, ?)", 
                       (usuario, pwd_hash, fecha))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": f"Usuario {usuario} registrado con exito"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"mensaje": "El usuario ya existe"}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    password = data.get('password')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM usuarios WHERE usuario = ?", (usuario,))
    record = cursor.fetchone()
    conn.close()

    if record and record[0] == hash_password(password):
        return jsonify({"mensaje": "Validacion exitosa"}), 200
    else:
        return jsonify({"mensaje": "Usuario/contrasena invalidos"}), 401

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)