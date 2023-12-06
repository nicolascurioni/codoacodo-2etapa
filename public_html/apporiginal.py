from flask import Flask, request, jsonify, render_template, redirect, url_for, session, abort
from flask_cors import CORS
from flask_session import Session
import mysql.connector

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = None
Session(app)

class GestorUsuarios:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario VARCHAR(255) NOT NULL,
            contrasena VARCHAR(255) NOT NULL,
            nombre VARCHAR(255),
            apellido VARCHAR(255),
            direccion VARCHAR(255),
            ciudad VARCHAR(255),
            provincia VARCHAR(255),
            telefono VARCHAR(20))
                            ''')
        self.conn.commit()

    def agregar_usuario(self, usuario, contrasena, nombre, apellido, direccion, ciudad, provincia, telefono):
        sql = "INSERT INTO usuarios (usuario, contrasena, nombre, apellido, direccion, ciudad, provincia, telefono) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (usuario, contrasena, nombre, apellido, direccion, ciudad, provincia, telefono)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True

    def consultar_usuario(self, usuario):
        self.cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
        return self.cursor.fetchone()

    def consultar_usuario_por_id(self, usuario_id):
        self.cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
        return self.cursor.fetchone()

    def verificar_credenciales(self, usuario, contrasena):
        sql = "SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s"
        valores = (usuario, contrasena)
        self.cursor.execute(sql, valores)
        return self.cursor.fetchone()

    def eliminar_usuario(self, usuario_id):
        sql = "DELETE FROM usuarios WHERE id = %s"
        self.cursor.execute(sql, (usuario_id,))
        self.conn.commit()
        print(f"Usuario eliminado correctamente. Usuario ID: {usuario_id}")
        return True
    
    def actualizar_usuario(self, usuario_info):
        sql = """
            UPDATE usuarios
            SET usuario = %s, contrasena = %s, nombre = %s, apellido = %s,
                direccion = %s, ciudad = %s, provincia = %s, telefono = %s
            WHERE id = %s
        """
        valores = (
            usuario_info['usuario'],
            usuario_info['contrasena'],
            usuario_info['nombre'],
            usuario_info['apellido'],
            usuario_info['direccion'],
            usuario_info['ciudad'],
            usuario_info['provincia'],
            usuario_info['telefono'],
            usuario_info['id']
        )

        self.cursor.execute(sql, valores)
        self.conn.commit()


gestor_usuarios = GestorUsuarios(host='localhost', user='root', password='', database='miapp')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')

    usuario_info = gestor_usuarios.verificar_credenciales(usuario, contrasena)
    if usuario_info:
        session['usuario_id'] = usuario_info['id']
        return jsonify(authenticated=True, redirect_url=url_for('perfil', _external=True))
    else:
        usuario_existente = gestor_usuarios.consultar_usuario(usuario)
        if usuario_existente:
            return jsonify(error_message="Credenciales incorrectas"), 401
        else:
            return jsonify(error_message="Usuario inexistente"), 404
        

@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    try:
        data = request.form
        usuario = data.get('usuario')
        contrasena = data.get('contrasena')
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        direccion = data.get('direccion')
        ciudad = data.get('ciudad')
        provincia = data.get('provincia')
        telefono = data.get('telefono')

        gestor_usuarios.agregar_usuario(usuario, contrasena, nombre, apellido, direccion, ciudad, provincia, telefono)

        return jsonify(message="Usuario agregado correctamente"), 200
    except Exception as e:
        return jsonify(error_message=str(e)), 500

@app.route('/perfil.html')
def perfil():
    usuario_id = session.get('usuario_id')
    usuario_info = gestor_usuarios.consultar_usuario_por_id(usuario_id)

    if usuario_info:
        return render_template('perfil.html', usuarioInfo=usuario_info)
    else:
        return redirect(url_for('index'))

@app.route('/editar.html')
def editar():
    usuario_id = session.get('usuario_id')
    usuario_info = gestor_usuarios.consultar_usuario_por_id(usuario_id)

    if usuario_info:
        return render_template('editar.html', usuarioInfo=usuario_info)
    else:
        return redirect(url_for('index'))

@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    usuario_id_autenticado = session.get('usuario_id')

    if usuario_id_autenticado is None:
        return jsonify(error_message="Usuario no autenticado"), 401

    data = request.json
    usuario_id_a_eliminar = data.get('usuario_id')

    print(f"Usuario autenticado: {usuario_id_autenticado}")
    print(f"Usuario a eliminar: {usuario_id_a_eliminar}")

    usuario_eliminado = gestor_usuarios.eliminar_usuario(usuario_id_a_eliminar)

    if usuario_eliminado:
        session.clear()
        return jsonify(message="Usuario eliminado correctamente")
    else:
        return jsonify(error_message="Error al eliminar el usuario"), 500


@app.route('/actualizar_usuario', methods=['POST'])
def actualizar_usuario():
    try:
        usuario_id = session.get('usuario_id')
        usuario_info = gestor_usuarios.consultar_usuario_por_id(usuario_id)

        if usuario_info:
            data = request.form
            usuario_info['usuario'] = data.get('usuario')
            usuario_info['contrasena'] = data.get('contrasena')
            usuario_info['nombre'] = data.get('nombre')
            usuario_info['apellido'] = data.get('apellido')
            usuario_info['direccion'] = data.get('direccion')
            usuario_info['ciudad'] = data.get('ciudad')
            usuario_info['provincia'] = data.get('provincia')
            usuario_info['telefono'] = data.get('telefono')

            gestor_usuarios.actualizar_usuario(usuario_info)

            return jsonify(message="Usuario actualizado correctamente"), 200
        else:
            return jsonify(error_message="Usuario no encontrado"), 404
    except Exception as e:
        return jsonify(error_message=str(e)), 500



@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

if __name__ == "__main__":
    app.run(debug=True)
