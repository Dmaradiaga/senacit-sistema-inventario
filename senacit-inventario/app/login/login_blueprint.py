from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from app.db.db import db
from app.login.form.login_formulario import FormularioLogin
from app.funciones_ayuda.funciones_ayuda import validar_valores_no_vacios,\
comprobar_hash_contrasena


login_bp = Blueprint('login_bp', __name__,
                        template_folder='templates',
                        static_folder='static'
                    )


# Ruta maneja el login al sistema de inventario
@login_bp.route('/', methods=["GET","POST"])
def index():
    form = FormularioLogin()
    if request.method=="POST":
        datos_login = {
            "contrasena": form.contrasena.data.strip(),
            "numero_identidad": form.numero_identidad.data
        }

        estado_valores = validar_valores_no_vacios(datos_login)
        
        if estado_valores:
            registro = db.login_inventario(datos_login["numero_identidad"])
            print("REGISTRO DEL USUARIO LOGIN: ",registro)
            if registro:
                estado_contrasena = comprobar_hash_contrasena(datos_login["contrasena"], registro[3])
                if estado_contrasena:
                    session["tipo_usuario"] = registro[4]
                    session["codigo_usuario"] = registro[2]
                    session["nombre_usuario"] = registro[0]
                    session["apellido_usuario"] = registro[1]
                    session["departamento_interno"] = registro[5]
                    session["id_usuario"] = registro[6]
                    session["id_imagen_url"] = registro[7]
                    session["url_firma_imagen"] = registro[8]
                    session["es_jefe_departamento"] = registro[9]
                    session["es_tecnico"] = registro[10]
                    session["correo"] = registro[11]


                    print("Se creó la sesión del usuario")
                    # Aquí redirige a la página de inicio de sesión exitosa
                    return redirect(url_for('agregar_registro_bp.index'))
                else:
                    flash("Número de identidad y/o contraseña incorrectas.", "warning")
                    return render_template('login.html', form=form)  
            else:
                flash("Número de identidad y/o contraseña incorrectas.", "warning")
                return render_template('login.html', form=form)
        else:
            flash("Debes ingresar los datos", "warning")
            return render_template('login.html', form=form)
    else:
        if 'tipo_usuario' in session:
          return redirect(url_for('agregar_registro_bp.index'))    
        return render_template('login.html', form=form)



# Ruta maneja el logout al sistema de inventario
@login_bp.route('/salir', methods=["GET"])
def logout():
    if 'tipo_usuario' in session or 'codigo_usuario' in session:
        # Elimina todas las variables de sesión
        session.clear()
        print("Sesión eliminada")
        return redirect(url_for('login_bp.index'))
    # Redirigir a la página de inicio de sesión
    return redirect(url_for('login_bp.index'))


