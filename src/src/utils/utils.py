from functools import wraps
from flask import request, redirect, url_for
from flask_login import current_user


def roles_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Verifica si el usuario tiene un rol válido para acceder a la vista
            if current_user.role in roles:
                return func(*args, **kwargs)
            else:
                # Si el usuario no tiene el rol correcto, redirige a una página de error o a otra vista apropiada
                print("Rol del usuario de el role requiered:", current_user.role, current_user.username, current_user.id)
                return redirect(url_for('acceso_denegado'))
        return wrapper
    return decorator
