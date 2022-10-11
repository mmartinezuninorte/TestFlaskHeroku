from flask import Flask, make_response, render_template, flash, g, url_for, redirect, session
from formularios import Login, Registro
from database import registrarUsuario, validarUsuario, usuarioSesionActual
import yagmail as yagmail
import os
from werkzeug.security import generate_password_hash
import functools


app=Flask(__name__)
app.secret_key = os.urandom(24)


def login_required(view):
    @functools.wraps(view)
    def warapped_view(**kwargs):
        if g.user is None:
            flash ("Para acceder a esta funcionalidad necesitas estar logueado")
            return redirect(url_for('login'))
        return view(**kwargs)
    return warapped_view

    
@app.route('/')
@login_required
def index():
    titulo='InventariosAPP'
    return render_template('index.html',titulo=titulo)

@app.before_request
def verificarUsuarioLogueado():
    #Parametrizacion para SQL de ubicacion BD
    g.PatchBaseDatos = 'baseDatosPrincipal.db'
    #Obtener y verificar usuario actual de la session
    user_id= session.get('user_id')
    if user_id is None:
        g.user=None
    else:
        g.user= usuarioSesionActual(user_id)


@app.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesion de manera correcta")
    return redirect(url_for('login'))




@app.route('/registro/', methods=['GET','POST'])
def registro():
    form=Registro()
    try:
        if (form.validate_on_submit()):
            name=form.name.data
            username=form.username.data
            email=form.email.data
            password=form.password.data
            print(name,username,email,password)
            passwordHash=generate_password_hash(password)
            registrarUsuario(name,username,email,passwordHash)
            yag=yagmail.SMTP('uninortepruebasciclo3@gmail.com' , 'taougyvfvxjvfndp')
            yag.send(to= email,
            subject=f"Bienvenido {username}",
            contents=f'<h1>Gracias por registrarte!</h1><br><h2>Bienvenido a nuestra App, esperamos sea de utilidad</h2>')
            flash ('Registro exitoso por favor verifique su correo')
            return render_template('registro.html', form=form)
    except:
        flash ("Opps ocurrio un error, parece que ya estas registrado!")
        return render_template('registro.html',form=form)
    return render_template('registro.html', form=form)


@app.route('/login/', methods=['GET','POST'])
def login():
    form=Login()
    try:
        if g.user:
            flash("Ya tienes una sesion iniciada!")
            return redirect (url_for('index'))
        if (form.validate_on_submit()):
            try:
                email= form.email.data
                password = form.password.data
                comprobacion=validarUsuario(email,password)
                if comprobacion:
                    session.clear()
                    session['user_id']=email
                    resp= make_response(redirect(url_for('index')))
                    resp.set_cookie('username',email)
                    flash ('Gracias por iniciar sesion')
                    return resp
                flash ("Email o password incorrectos")
                return render_template('login.html',form=form)
            except:
                flash('Opps algo salio mal, Cod=ErorValidacion00x.')
        return render_template('login.html',form=form)
    except:
        flash("Opps error inesperado, reintenta o contactate con soporte")
        return render_template('login.html',form=form)

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('server.cer','server.key'))