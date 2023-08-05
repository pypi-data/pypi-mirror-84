from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps
from models.user import Roles


# Decorator per controllare il ruolo di un utente e se questo
# sia autenticato oppure no
def role_required(role):
    def wrapper(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            temp_role = ''
            if isinstance(role, Roles):
                temp_role = [role]
            else:
                temp_role = role
            if (current_user.is_authenticated and (current_user.role in temp_role)):
                return f(*args, **kwargs)
            flash("Non hai i permessi per accedere a questa pagina")
            return redirect(url_for('home'))
        return wrap
    return wrapper
