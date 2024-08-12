from flask import Blueprint, session,redirect,url_for
from functools import wraps


autorizacion_bp = Blueprint('autorizacion_bp', __name__,
                        template_folder='templates',
                        static_folder='static')


# Función decoradora para verificar si el usuario tiene sesión
def comprobando_autorizacion(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'tipo_usuario' in session:
            return view(*args, **kwargs)
        else:
            # Redirigir al login
            return redirect(url_for('login_bp.index'))
    return wrapped_view


# Función decoradora para verificar si el usuario normal es técnico
def es_tecnico(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'es_tecnico' in session and session['es_tecnico']==1 or \
            'tipo_usuario' in session and session['tipo_usuario']=='Administrador':
            return view(*args, **kwargs)
        else:
            # Redirigir a consultas
            return redirect(url_for('consultas_bp.index'))
    return wrapped_view



# Función decoradora para verificar si el usuario tiene sesión y es el administrador
def comprobando_sesion_administrador(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'tipo_usuario' in session and session['tipo_usuario']=='Administrador':
            return view(*args, **kwargs)
        elif 'tipo_usuario' in session and session['tipo_usuario']=='Usuario Normal':
            return redirect(url_for('consultas_bp.index'))
        else:
            # Redirigir a una página de acceso denegado u otra página relevante
            return redirect(url_for('login_bp.index'))
    return wrapped_view 

