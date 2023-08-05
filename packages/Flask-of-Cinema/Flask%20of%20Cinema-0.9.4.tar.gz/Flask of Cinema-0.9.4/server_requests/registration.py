import db_init
import re
from flask import flash
from db import create_conn, update_conn
from models.user import User
from sqlalchemy.sql import Select
from werkzeug.security import generate_password_hash


# Inserisce un nuovo utente nel db se tutti i controlli passano
def insert_user(user: User, oldEmail: str = None):
    # noqa pylint: disable=no-value-for-parameter
    ins = db_init.users.insert()
    conn = create_conn()
    existingUser = conn.execute(Select([db_init.users.c.email]).where(
        db_init.users.c.email == user['email'])).fetchone()
    # Non aggiunge un nuovo utente se: esiste già nel db, la password non ha superato il controllo e la mail non è valida
    # noqa pylint: disable=no-else-return
    if existingUser is None and oldEmail is None and password_check(user['password']) and email_check(user['email']):
        update_conn(conn, "READ COMMITTED")
        conn.execute(ins, [
            {'email': user['email'], 'firstName': user['firstName'], 'lastName': user['lastName'],
             'password': generate_password_hash(user['password']), 'role': user['role']}
        ])
        conn.close()
        return user
    # Se viene passata una oldEmail sto cercando di modificare l'utente, quindi eseguo la modifica
    elif (existingUser is None or user["email"] == oldEmail) and oldEmail is not None and email_check(user['email']):
        update_conn(conn, "READ COMMITTED")
        # noqa pylint: disable=no-value-for-parameter
        conn.execute(db_init.users.update().where(db_init.users.c.email == oldEmail).values(
            email=user['email'], firstName=user['firstName'], lastName=user['lastName']))
        conn.close()
        return user
    # Se viene trovato già un utente, significa che la mail è utilizzata
    elif existingUser is not None:
        flash('Esiste già un utente con questa email', "user-error")
        conn.close()
        return None
    elif not email_check(user['email']):
        flash('La mail non è valida', "user-error")
        conn.close()
        return None
    flash('La password deve avere almeno 5 caratteri ed una cifra', "user-error")
    conn.close()
    return None


# Controllo che la password rispetti le policy di sicurezza
def password_check(password: str):
    if (len(password) > 4) & any(char.isdigit() for char in password):
        return True
    return False


# Controllo che la mail sia valida
def email_check(email: str):
    regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    if(re.search(regex, email)):
        return True
    return False
