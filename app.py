from flask import Flask, render_template, request, redirect, url_for
import redis
import uuid

app = Flask(__name__)

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Mostrar todos los usuarios
@app.route('/')
def index():
    claves = r.keys("usuario:*")
    usuarios = []
    for clave in claves:
        usuario = r.hgetall(clave)
        usuario['id'] = clave.split(":")[1]
        usuarios.append(usuario)
    return render_template('index.html', usuarios=usuarios)

# Mostrar formulario
@app.route('/crear')
def crear():
    return render_template('form.html', usuario=None)

# Guardar nuevo usuario
@app.route('/guardar', methods=['POST'])
def guardar():
    id = str(uuid.uuid4())[:8]  # Genera ID único corto
    nombre = request.form['nombre']
    edad = request.form['edad']
    ciudad = request.form['ciudad']

    r.hset(f"usuario:{id}", mapping={
        "nombre": nombre,
        "edad": edad,
        "ciudad": ciudad
    })
    return redirect(url_for('index'))

# Mostrar formulario con datos existentes
@app.route('/editar/<id>')
def editar(id):
    usuario = r.hgetall(f"usuario:{id}")
    usuario['id'] = id
    return render_template('form.html', usuario=usuario)

# Guardar cambios
@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    nombre = request.form['nombre']
    edad = request.form['edad']
    ciudad = request.form['ciudad']
    r.hset(f"usuario:{id}", mapping={
        "nombre": nombre,
        "edad": edad,
        "ciudad": ciudad
    })
    return redirect(url_for('index'))

# Eliminar usuario
@app.route('/eliminar/<id>')
def eliminar(id):
    r.delete(f"usuario:{id}")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
