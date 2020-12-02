from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'spbYO0JJOPUFLUikKYbKrpS5w3KUEnab5KcYDdYb'
db = sqlite3.connect('data.db', check_same_thread=False)

# Rutas
@app.route('/', methods=['GET']) # / significa la ruta raiz
def index():
    return render_template('index.html')

@app.route('/saludo/<nombre>/<int:edad>') # Nombre
def saludar(nombre, edad):
    numeros = [1,2,3,4,5,6,7,8,9]
    return render_template('saludo.html', name=nombre, age=edad, numbers=numeros)

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    #Obteniendo formulario de contacto
    if request.method == 'GET':
        return render_template('contacto.html')
    
    #Guardando la información de contacto
    nombres = request.form.get('nombres')
    email = request.form.get('email')
    celular = request.form.get('celular')
    observacion = request.form.get('observacion')

    return 'Guardando información ' + observacion
    
@app.route('/sumar')
def sumar():
    resultado = 2+2
    return 'la suma de 2+2=' + str(resultado)

@app.route('/usuarios')
def usuarios():
    usuarios = db.execute('select * from usuarios')

    usuarios = usuarios.fetchall()

    return render_template('usuarios/listar.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuarios():
    if request.method == 'GET':
        return render_template('usuarios/crear.html')
    
    nombres = request.form.get('nombres')
    apellidos = request.form.get('apellidos')
    email = request.form.get('email')
    password = request.form.get('password')

    #Validando que el correo no este en uso
    usuario = db.execute('select * from usuarios where email = ?', (email,)).fetchall()

    if(nombres == ""):
        flash('El campo nombres es requerido', 'error')
        return redirect(request.url)

    if(len(usuario) > 0):
        flash('Ya existe un usuario con este email', 'error')
        return redirect(request.url)

    try:
        cursor = db.cursor()
        cursor.execute("""insert into usuarios(
                nombres,
                apellidos,
                email,
                password
            )values (?,?,?,?)
        """, (nombres, apellidos, email, password,))

        db.commit()
    except:
        flash('No se ha podido guardar el usuario', 'error')
        return redirect(url_for('usuarios'))

    flash('Usuario creado correctamente', 'success')

    return redirect(url_for('usuarios'))

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if request.method == 'GET':
        usuario = db.execute('select * from usuarios where id = ?', (id,)).fetchone()
        
        return render_template('usuarios/editar.html', usuario=usuario)

    nombres = request.form.get('nombres')
    apellidos = request.form.get('apellidos')
    email = request.form.get('email')
    # password = request.form.get('password')

    cursor = db.cursor()
    cursor.execute("""update usuarios set nombres = ?,
        apellidos = ?, email = ? where id = ? 
    """, (nombres, apellidos, email, id,))

    db.commit()

    flash('Usuario editado correctamente', 'success')

    return redirect(url_for('usuarios'))

app.run(debug=True)