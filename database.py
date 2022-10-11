import sqlite3 as sql
from sqlite3 import Error
from werkzeug.security import check_password_hash
from flask import g

#Sentencias para creacion de Base de datos y Tablas de forma general
####################################################################

#Crea la base de datos con el nombre indicado
def crearBD(nombreBD):
    try:
        conn=sql.connect(nombreBD)
        conn.commit()
        conn.close()
    except Error:
        print(Error)

#Crea la tabala regUsuarios para almacenar usuarios registrados
def crearTablaRegUsuarios():
    conn=sql.connect(g.PatchBaseDatos)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE regUsuarios(
            name text,
            username text,
            email text primary key,
            password text
        )
    """
    )
    conn.commit()
    conn.close()


#Metodos para usar la tabla regUsuarios
#######################################

# Registro de nuevos usuarios en la tabla regUsuarios
# basandonos en la estructura inicial de la misma
def registrarUsuario(name, username, email, password):
    conn=sql.connect(g.PatchBaseDatos)
    cursor = conn.cursor()
    instruccion= f"INSERT INTO regUsuarios VALUES('{name}','{username}','{email}','{password}')"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


# Validacion de contraseña de usuario para el login
# Devuelve True or false en base a la comparacion directa
def validarUsuario(email,password):
    conn=sql.connect(g.PatchBaseDatos)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM regUsuarios WHERE email ='{email}'"
    cursor.execute(instruccion)
    user=cursor.fetchone()
    if user is None:
        conn.commit()
        conn.close()
        return False
    capturarContrasena=user[3]
    comparacionHashContrasena=check_password_hash(capturarContrasena,password)
    conn.commit()
    conn.close()
    if comparacionHashContrasena is False:
        return False
    else:
        return True

# Encuentra la informacion referente al usuario actual en sesion
# y lo retorna al sitio de llamado
def usuarioSesionActual(usuarioActual):
    conn=sql.connect(g.PatchBaseDatos)
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM regUsuarios WHERE email ='{usuarioActual}'"
    cursor.execute(instruccion)
    user=cursor.fetchone()
    conn.commit()
    conn.close()
    return ( user )




## Metodos en deshuso
#def insertarProducto(nombre, valor, cantidad):
#    conn=sql.connect('inventario.db')
#    cursor = conn.cursor()
#    instruccion= f"INSERT INTO productos VALUES('{nombre}',{valor},{cantidad})"
#    cursor.execute(instruccion)
#    conn.commit()
#    conn.close()

#def insertarVariosProductos(listaProductos):
#    conn=sql.connect('inventario.db')
#    cursor = conn.cursor()
#    instruccion = f"INSERT INTO productos VALUES(? ,? ,? )"
#    cursor.executemany(instruccion, listaProductos)
#    conn.commit()
#    conn.close()

#def leerValoresProductos():
#    conn=sql.connect('inventario.db')
#    cursor = conn.cursor()
#    instruccion = f"SELECT * FROM productos"
#    cursor.execute(instruccion)
#    datos=cursor.fetchall()
#    conn.commit()
#    conn.close()
#    return datos

#def actualizarProducto():
#    conn=sql.connect('inventario.db')
#    cursor = conn.cursor()
#    instruccion = f"UPDATE productos SET valor=90000 WHERE nombre ='Audifonos'"
#    cursor.execute(instruccion)
#    conn.commit()
#    conn.close()

#def eliminarProducto():
#    conn=sql.connect('inventario.db')
#    cursor = conn.cursor()
#    instruccion = f"DELETE FROM productos WHERE nombre = 'Audifonos'"
#    cursor.execute(instruccion)
#    conn.commit()
#    conn.close()

