from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.exceptions import abort
import sqlite3


from typing import Union

from fastapi import FastAPI

import sqlite3

from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Esthefania_blog'

#DB Conection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#Get ID from post_id
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)

    return post

#Index
@app.route("/")
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

#See a specific post
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

#Create a post
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
      title = request.form['title']
      content = request.form['content']
      tags = request.form['tags']
      coments = request.form['coments']

      if not title:
          flash('TU PUBLICACIÓN DEBE TENER UN TÍTULO')
      else:
          conn = get_db_connection()
          conn.execute('INSERT INTO posts(title, content, tags, coments) VALUES (?, ?, ?, ?)',
                       (title, content, tags, coments))
          conn.commit()
          conn.close()
          return redirect(url_for('index'))

    return render_template('create.html')

#Edit post
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('TU PUBLICACIÓN DEBE TENER UN TÍTULO')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

#Delete post
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" fue eliminado.'.format(post['title']))
    return redirect(url_for('index'))

#Error pages
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

#Credits
@app.route("/credits")
def credits():
    return render_template('credits.html')

if __name__ == '__main__':
    app.run(debug=True)

app = FastAPI()

# Configuración de CORS para permitir solicitudes desde cualquier origen ('*')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Esto permite todas las solicitudes desde cualquier origen
    allow_methods=["*"],  # Esto permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Esto permite todos los encabezados HTTP
    allow_credentials=False,  # Si estás manejando autenticación con cookies u otros medios, puedes establecer esto en True
    expose_headers=None,
    max_age=None,
)

def createTable():
    # Conectar a la base de datos o crearla si no existe
    conn = sqlite3.connect("inventario.db")
    # Crear un cursor para interactuar con la base de datos
    cursor = conn.cursor()
    # Crear la tabla "users" con los campos especificados
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    username TEXT NOT NULL,
                    contraseña TEXT NOT NULL
                )''')
    # Guardar los cambios en la base de datos
    conn.commit()
    # Cerrar la conexión a la base de datos
    conn.close()

    # Conectar a la base de datos o crearla si no existe
    conn = sqlite3.connect("inventario.db")
    # Crear un cursor para interactuar con la base de datos
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                    producto_id INTEGER  PRIMARY KEY,
                    nombre TEXT UNIQUE,
                    precio REAL NOT NULL
                )''')
    # Guardar los cambios en la base de datos
    conn.commit()
    # Cerrar la conexión a la base de datos
    conn.close()

    # Conectar a la base de datos o crearla si no existe
    conn = sqlite3.connect("inventario.db")
    # Crear un cursor para interactuar con la base de datos
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores (
                    proveedor_id INTEGER  PRIMARY KEY,
                    nombre VARCHAR(50) NOT NULL UNIQUE,
                    telefono VARCHAR(20) NOT NULL UNIQUE
                    )''')
    # Guardar los cambios en la base de datos
    conn.commit()
    # Cerrar la conexión a la base de datos
    conn.close()

    # Conectar a la base de datos o crearla si no existe
    conn = sqlite3.connect("inventario.db")
    # Crear un cursor para interactuar con la base de datos
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores_productos (
                    proveedor_id INTEGER,
                    producto_id INTEGER,
                    FOREIGN KEY (proveedor_id) REFERENCES proveedores (proveedor_id),
                    FOREIGN KEY (producto_id) REFERENCES productos (producto_id),
                    PRIMARY KEY (proveedor_id, producto_id)
                )''')

    # Guardar los cambios en la base de datos
    conn.commit()
    # Cerrar la conexión a la base de datos
    conn.close()

createTable()

class User(BaseModel):
    nombre: str
    username: str
    contraseña: str
    
class Producto(BaseModel):
    producto_id:int
    nombre_producto: str
    precio_producto: float
    
class Proveedor(BaseModel):
    proveedor_id:int
    nombre_proveedor: str
    telefono_proveedor: str        
class ProveedoresProductos(BaseModel):
    nombre_producto: str
    precio_producto: float
    nombre_proveerdor: str
    telefono_proveedor: str    
@app.post("/user/register")
async def crear_usuario(user:User):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Iniciar una transacción
        conn.execute("BEGIN")

        # Insertar un nuevo usuario en la tabla "users"
        cursor.execute("INSERT INTO users (nombre, username, contraseña) VALUES (?, ?, ?)",
                       (user.nombre, user.username, user.contraseña))

        # Confirmar la transacción
        conn.commit()

        print("Usuario creado exitosamente.")

    except sqlite3.Error as e:
        # En caso de un error, realizar un rollback para deshacer cualquier cambio
        conn.rollback()
        print("Error durante la creación del usuario:", e)

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()
        
@app.post("/user/iniciarsesion")
async def iniciar_sesion(user:User):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Consultar la tabla "users" para verificar las credenciales
        cursor.execute("SELECT * FROM users WHERE username = ? AND contraseña = ?", (user.username, user.contraseña))

        # Obtener el resultado de la consulta
        usuario = cursor.fetchone()

        if usuario:
            print("Inicio de sesión exitoso. ¡Bienvenido,", usuario[1] + "!")  # usuario[1] es el campo "nombre"
            return "sucess"  # usuario[1] es el campo "nombre"
        else:
            return "Credenciales incorrectas. Por favor, verifique su nombre de usuario y contraseña."

    except sqlite3.Error as e:
        print("Error durante el inicio de sesión:", e)

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()

@app.get("/productos")
async def obtenerProductos():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Consulta SQL para obtener todos los productos
        consulta = "SELECT * FROM productos"
        
        # Ejecutar la consulta y obtener los resultados
        cursor.execute(consulta)
        productos:Producto = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        conn.close()

        # Formatear los resultados como un array de objetos JSON
        productos_json = []
        for producto in productos:
            producto_dict = {
                "id": producto[0],
                "nombre": producto[1],
                "precio": producto[2]
            }
            productos_json.append(producto_dict)

        return productos_json
    except sqlite3.Error as e:
        print("Error al obtener los productos:", e)
        return e
@app.get("/productos/{proveedor_id}")
def obtener_productos_de_proveedor(proveedor_id):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        
        # Realizar una consulta para obtener los productos del proveedor
        cursor.execute("""
            SELECT productos.*
            FROM productos
            JOIN proveedores_productos ON productos.producto_id = proveedores_productos.producto_id
            WHERE proveedores_productos.proveedor_id = ?
        """, (proveedor_id,))
        

        # Obtener todos los productos relacionados con el proveedor
        productos = cursor.fetchall()
        productos_json = []
        for producto in productos:
            producto_dict = {
                "id": producto[0],
                "nombre": producto[1],
                "precio": producto[2]
            }
            print(producto)
            print(producto_dict)
            productos_json.append(producto_dict)
        print(productos_json)
        return productos_json

    except sqlite3.Error as e:
        print("Error al obtener los productos:", e)

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()
                    
@app.get("/proveedores")
async def obtenerProveedores():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Consulta SQL para obtener todos los proveedores
        consulta = "SELECT * FROM proveedores"
        
        # Ejecutar la consulta y obtener los resultados
        cursor.execute(consulta)
        proveedores = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        conn.close()
        
        # Formatear los resultados como un array de objetos JSON
        proveedores_json = []
        for proveedor in proveedores:
            proveedor_dict = {
                "id": proveedor[0],
                "nombre": proveedor[1],
                "telefono": proveedor[2]
            }
            proveedores_json.append(proveedor_dict)

        return proveedores_json
    except sqlite3.Error as e:
        print("Error al obtener los proveedores:", e)
        return e
@app.get("/proveedores/{producto_id}")
def obtener_proveedores_de_producto(producto_id):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Realizar una consulta para obtener los proveedores del producto
        cursor.execute("""
            SELECT proveedores.*
            FROM proveedores
            JOIN proveedores_productos ON proveedores.proveedor_id = proveedores_productos.proveedor_id
            WHERE proveedores_productos.producto_id = ?
        """, (producto_id,))

        # Obtener todos los proveedores relacionados con el producto
        proveedores = cursor.fetchall()

         # Formatear los resultados como un array de objetos JSON
        proveedores_json = []
        for proveedor in proveedores:
            proveedor_dict = {
                "id": proveedor[0],
                "nombre": proveedor[1],
                "telefono": proveedor[2]
            }
            proveedores_json.append(proveedor_dict)

        return proveedores_json

    except sqlite3.Error as e:
        print("Error al obtener los proveedores:", e)

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()





@app.post("/guardar")
async def insertar_proveedores_productos(inventario:ProveedoresProductos):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Iniciar una transacción
        conn.execute("BEGIN")

        # Insertar el proveedor si no existe
        cursor.execute("INSERT OR IGNORE INTO proveedores (nombre, telefono) VALUES (?, ?)",
                       (inventario.nombre_proveerdor, inventario.telefono_proveedor))
           
        # Obtener el ID del proveedor existente o recién insertado
        cursor.execute("SELECT proveedor_id FROM proveedores WHERE nombre = ?", (inventario.nombre_proveerdor,))
        proveedor_id = cursor.fetchone()[0]
        

        # Insertar el producto si no existe
        cursor.execute("INSERT OR IGNORE INTO productos (nombre, precio) VALUES (?, ?)",
                       (inventario.nombre_producto, inventario.precio_producto))

        # Obtener el ID del producto existente o recién insertado
        cursor.execute("SELECT producto_id FROM productos WHERE nombre = ?", (inventario.nombre_producto,))
        producto_id = cursor.fetchone()[0]

        # Insertar la relación entre producto y proveedor en la tabla de relación si no existe
        cursor.execute("INSERT OR IGNORE INTO proveedores_productos (producto_id, proveedor_id) VALUES (?, ?)",
                       (producto_id, proveedor_id))

        # Confirmar la transacción
        conn.commit()

        print("Inserciones completadas exitosamente.")

    except sqlite3.Error as e:
        # En caso de un error, realizar un rollback para deshacer cualquier cambio
        conn.rollback()
        print("Error durante la inserción:", e)

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()

@app.delete("proveedores/borrar/{proveedor_id}")
async def eliminar_proveedor_y_productos_asociados(proveedor_id):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Iniciar una transacción
        conn.execute("BEGIN")

        # Eliminar los registros de productos asociados al proveedor
        cursor.execute("DELETE FROM productos_proveedores WHERE proveedor_id = ?", (proveedor_id,))

        # Eliminar el proveedor de la tabla "proveedores"
        cursor.execute("DELETE FROM proveedores WHERE proveedor_id = ?", (proveedor_id,))

        # Opcionalmente, eliminar los productos que no están relacionados con otros proveedores
        # cursor.execute("DELETE FROM productos WHERE producto_id NOT IN (SELECT producto_id FROM productos_proveedores)")

        # Confirmar la transacción
        conn.commit()

        print(f"Proveedor con ID {proveedor_id} y sus productos asociados fueron eliminados.")

    except sqlite3.Error as e:
        # En caso de un error, realizar un rollback para deshacer cualquier cambio
        conn.rollback()
        print("Error durante la eliminación:", e)

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()

@app.delete("productos/borrar/{producto_id}")
async def eliminar_producto_y_proveedores_asociados(producto_id):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Iniciar una transacción
        conn.execute("BEGIN")

        # Eliminar los registros en la tabla de relación "productos_proveedores" relacionados con el producto
        cursor.execute("DELETE FROM productos_proveedores WHERE producto_id = ?", (producto_id,))

        # Eliminar el producto de la tabla "productos"
        cursor.execute("DELETE FROM productos WHERE producto_id = ?", (producto_id,))

        # Confirmar la transacción
        conn.commit()

        print(f"Producto con ID {producto_id} y sus proveedores asociados fueron eliminados.")

    except sqlite3.Error as e:
        # En caso de un error, realizar un rollback para deshacer cualquier cambio
        conn.rollback()
        print("Error durante la eliminación:", e)

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()
        

@app.put("producto/modificar")
async def actualizar_producto(productoNuevo:Producto):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Iniciar una transacción
        conn.execute("BEGIN")

        # Actualizar el producto en la tabla "productos"
        cursor.execute("UPDATE productos SET nombre = ?, precio = ? WHERE producto_id = ?",
                       (productoNuevo.nombre_producto, productoNuevo.precio_producto, productoNuevo.producto_id))

        # Confirmar la transacción
        conn.commit()

        print(f"Producto con ID {productoNuevo.producto_id} actualizado exitosamente.")

    except sqlite3.Error as e:
        # En caso de un error, realizar un rollback para deshacer cualquier cambio
        conn.rollback()
        print("Error durante la actualización:", e)

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()
        
@app.put("proveedor/modificar")
async def actualizar_proveedor(proveedorNuevo:Proveedor):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Iniciar una transacción
        conn.execute("BEGIN")

        # Actualizar el proveedor en la tabla "proveedores"
        cursor.execute("UPDATE proveedores SET nombre = ?, telefono = ? WHERE proveedor_id = ?",
                       (proveedorNuevo.nombre_proveedor, proveedorNuevo.telefono_proveedor, proveedorNuevo.proveedor_id))

        # Confirmar la transacción
        conn.commit()

        print(f"Proveedor con ID {proveedorNuevo.proveedor_id} actualizado exitosamente.")

    except sqlite3.Error as e:
        # En caso de un error, realizar un rollback para deshacer cualquier cambio
        conn.rollback()
        print("Error durante la actualización:", e)

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()  
