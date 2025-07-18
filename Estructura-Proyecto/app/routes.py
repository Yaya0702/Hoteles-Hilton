from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .ext import mysql
from werkzeug.security import generate_password_hash, check_password_hash


routes = Blueprint('routes', __name__)

# ------------------------ LOGIN ------------------------
@routes.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['txtUser']
        contraseña = request.form['txtpassword']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Usuarios WHERE nombre_usuario = %s", (usuario,))
        user = cur.fetchone()

        if user:
            contraseña_hash = user[3]  
            if check_password_hash(contraseña_hash, contraseña) or contraseña_hash == contraseña:
                session['usuario'] = user[1]
                session['id_usuario'] = user[0]
                return redirect(url_for('routes.dashboard'))
        
        return render_template('Login.html')

    return render_template('Login.html')

# ------------------------ REGISTRO ------------------------
@routes.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre_usuario']
        correo = request.form['correo']
        contraseña = request.form['contraseña'] 
        
        
        pwd_hash = generate_password_hash(contraseña, method='pbkdf2:sha256')


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Usuarios (nombre_usuario, correo, contraseña_hash) VALUES (%s, %s, %s)",
                    (nombre, correo, pwd_hash )) 
        mysql.connection.commit()
        return redirect(url_for('routes.login'))

    return render_template('registro.html')


# ------------------------ LOGOUT ------------------------
@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes./'))
    

# ------------------------ DASHBOARD ------------------------
@routes.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('routes.login'))
    return render_template('Dashboard.html')


# ------------------------ CRUD: CATEGORÍAS ------------------------
@routes.route('/categorias')
def categorias():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM CategoriasHotel")
    categorias = cur.fetchall()
    return render_template('G.Categorias.html', categorias=categorias)


@routes.route('/agregar_categoria', methods=['POST'])
def agregar_categoria():
    nombre = request.form['nombre']
    estrellas = request.form['estrellas']
    descripcion = request.form['descripcion']
    servicios = request.form['servicios']
    iva = request.form['iva']
    id_usuario = session.get('id_usuario')

    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO CategoriasHotel (nombre_categoria, estrellas_o_tipo, descripcion_general, servicios_tipicos, iva_aplicable, id_usuario)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (nombre, estrellas, descripcion, servicios, iva, id_usuario))
    mysql.connection.commit()
    return redirect(url_for('routes.categorias'))


# ------------------------ CRUD: TIPOS DE HABITACIÓN ------------------------
@routes.route('/tipos_habitacion')
def tipos_habitacion():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM TiposHabitacion")
    tipos = cur.fetchall()
    return render_template('G.TipoHabitacion.html', tipos=tipos)


@routes.route('/agregar_tipo', methods=['POST'])
def agregar_tipo():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    id_usuario = session.get('id_usuario')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO TiposHabitacion (nombre_tipo, descripcion, id_usuario) VALUES (%s, %s, %s)",
                (nombre, descripcion, id_usuario))
    mysql.connection.commit()
    return redirect(url_for('routes.tipos_habitacion'))


# ------------------------ CRUD: HABITACIONES ------------------------
@routes.route('/habitaciones')
def habitaciones():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT h.*, t.nombre_tipo 
        FROM Habitaciones h
        JOIN TiposHabitacion t ON h.id_tipo_habitacion = t.id_tipo_habitacion
    """)
    habitaciones = cur.fetchall()
    return render_template('G.Habitaciones.html', habitaciones=habitaciones)


@routes.route('/agregar_habitacion', methods=['POST'])
def agregar_habitacion():
    codigo = request.form['codigo']
    numero = request.form['numero']
    piso = request.form['piso']
    estado = request.form['estado']
    tipo_id = request.form['tipo_id']
    id_usuario = session.get('id_usuario')

    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO Habitaciones (codigo_habitacion, id_tipo_habitacion, numero_habitacion, piso, estado, id_usuario)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (codigo, tipo_id, numero, piso, estado, id_usuario))
    mysql.connection.commit()
    return redirect(url_for('routes.habitaciones'))

