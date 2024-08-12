from flask import Blueprint, render_template, request, url_for, redirect, flash, session,g
from app.db.db import db
from app.reestablecer_contrasena.forms.reestablecer_contrasena_formulario import ReestablecerContrasenaFormulario
from app.funciones_ayuda.funciones_ayuda import encriptar_contrasena

from string import ascii_letters, digits
import random

#MailJet
from mailjet_rest import Client


reestablecer_contrasena_bp = Blueprint('reestablecer_contrasena_bp', __name__,
                        template_folder='templates',
                        static_folder='static'
                    )



#Genera caracteres alfanúmericos aleatorios de longitud 6
def generar_codigo():
    codigo = ''.join(random.choice(ascii_letters + digits) for i in range(6))
    return codigo


def enviar_correo(correo, codigo):

    api_key = g.app.config['MAILJET_API_KEY']
    api_secret = g.app.config['MAILJET_SECRET_KEY']

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    datos = {
    'Messages': [
        {
        "From": {
            "Email": "dmaradiaga08@gmail.com",
            "Name": "Senacithn"
        },
        "To": [
            {
                "Email": correo,
                "Name": "Para ti"
            }
        ],
            "Subject": "Reestablecer Contraseña",
            "HTMLPart": "<h3>El código solo es válido por 12 minutos.</h3><br /><b>Código: "+codigo+"</b>"
        }
      ]
    }
    resultado = mailjet.send.create(data=datos)
    print(resultado)
    return True


# Ruta maneja el reestablecer_contrasena 
@reestablecer_contrasena_bp.route('/', methods=["GET","POST"])
def index():
    form = ReestablecerContrasenaFormulario()
    if request.method=="POST":        
            correo = form.correo.data.strip()  
            if correo!="":
                registro = db.comprobar_usuario_correo(correo)

                if registro is None:
                    print("Registro: ", registro)
                    codigo = generar_codigo()
                    resultado_envio_correo = enviar_correo(correo,codigo)
                    if resultado_envio_correo:
                        datos_ingresar = { 'correo': correo, 'codigo': codigo }
                        estado_solicitud = db.agregar_codigo_reestablecer_contrasena(datos_ingresar)
                        if estado_solicitud:
                            flash("Se envió un código a tú correo","success")
                            return redirect(url_for('reestablecer_contrasena_bp.index'))
                        else:
                            flash("No se pudo procesar la solicitud. Vuelve a intentarlo","warning")
                            return render_template('reestablecer_contrasena.html', form=form)
                    else:
                        flash("No se pudo enviar el correo. Vuelve a intentarlo","warning")
                        return render_template('reestablecer_contrasena.html', form=form)
                else:
                    flash("Ya existe una solicitud con ese correo","warning")
                    return render_template('reestablecer_contrasena.html', form=form)
            else:
               flash("Debes ingresar el correo", "warning")
               return render_template('reestablecer_contrasena.html', form=form)

    else:   
        return render_template('reestablecer_contrasena.html', form=form)


# Ruta maneja el logout al sistema de inventario
@reestablecer_contrasena_bp.route('/nueva_contrasena', methods=["GET", "POST"])
def nueva_contrasena():
    form = ReestablecerContrasenaFormulario()
    if request.method=="POST":        
            verificar_contrasena = form.verificar_contrasena.data.strip()
            contrasena = form.contrasena.data.strip()
            codigo = form.codigo.data.strip()

            if codigo!="" and verificar_contrasena!="" and contrasena!="":
                
                if contrasena!=verificar_contrasena:
                    flash("Las contraseñas no coinciden","warning")
                    return render_template("nueva_contrasena.html", form=form)
                
                registro = db.comprobar_codigo_contrasena(codigo)
                print(registro)

                if registro:
                    contrasena_hash = encriptar_contrasena(contrasena)
                    datos_actualizar = {
                        "contrasena": contrasena_hash
                    }

                    estado_consulta = db.actualizar_contrasena(datos_actualizar, registro[1])
                    if estado_consulta:
                        estado_registro_eliminado = db.eliminar_registro_reestablecer_contrasena(registro[1])
                        if estado_registro_eliminado:     
                            flash("Enhorabuena se ha actualizado la contraseña.","success")
                            return redirect(url_for('login_bp.index'))
                        else:
                            flash("No se pudo actualizar la contraseña.","warning")
                            return render_template("nueva_contrasena.html", form=form)
                    else:
                        flash("No se pudo actualizar la contraseña.","warning")
                        return render_template("nueva_contrasena.html", form=form)
                else:
                    flash("Código Incorrecto","warning")
                    return render_template("nueva_contrasena.html", form=form)
            else:
                flash("Debes ingresar los datos","warning")
                return render_template("nueva_contrasena.html", form=form)
    else:   
        return render_template('nueva_contrasena.html', form=form)


