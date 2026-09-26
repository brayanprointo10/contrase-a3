from flask import Flask, render_template, request, redirect, url_for, flash, session
from consultas import consulta, insertar         
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesaria para usar flash

@app.route('/')
def inicio():
    #query = 'SELECT * FROM servicios'
    servicios = [{"id": 1, "nombre": "Servicio 1", "descripcion": "Descripción del servicio 1"},
                 {"id": 2, "nombre": "Servicio 2", "descripcion": "Descripción del servicio 2"},]
    return render_template('index.html', servicios=servicios)

@app.route('/nosotros')
def nosotros():
    return render_template('paginas/nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('paginas/contacto.html')

@app.route('/servicios')
def servicios():
    return render_template('paginas/servicios.html')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    query = ('DELETE FROM servicios WHERE id = %s')
    parametros = (id,)
    insertar(query, parametros)
    return redirect('/')


@app.route("/insertar_registro", methods=['GET', 'POST'])

def insertar_servicio():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        query = ("INSERT INTO servicios (nombre, descripcion) VALUES (%s, %s)")
        parametros = (nombre, descripcion)
        insertar(query, parametros)
        flash('Servicio agregado correctamente.', 'exitoso')  # Mensaje de éxito
        return redirect(url_for('inicio'))
    else:    
        return render_template('admin/servicios.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuarios = request.form.get('usuario')
        contraseña = request.form.get('contraseña')
        query = 'SELECT usuarios, contraseña FROM usuarios WHERE usuarios = %s '
        parametros = (usuarios,)
        respuesta = consulta(query, parametros)
        

        if respuesta:
            clave = respuesta[0]['contraseña']
            if check_password_hash(clave,contraseña):
                flash('Inicio de sesión exitoso.', 'exitoso')
                session['user'] =[respuesta[0]['usuarios']]
                return redirect(url_for('insertar_servicio'))
            else:
                flash('Contraseña incorrecta.', 'error')
                return redirect(url_for('login'))
        else:
            flash('Usuario no encontrado.', 'error')
            return redirect(url_for('login'))

    else:
        print(generate_password_hash('1234'))
        return render_template('loguin.html')
@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'exitoso')
    return redirect(url_for('inicio'))

app.run(debug=True)