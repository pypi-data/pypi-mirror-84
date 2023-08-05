import db_init
from db import create_conn, update_conn
from flask import flash
from flask_login import login_user
from sqlalchemy.sql import Select
from werkzeug.security import check_password_hash, generate_password_hash
from server_requests.users import user_by_email
from server_requests.registration import password_check


# Controlla che le credenziali al login siano corrette
def check_credentials(email: str, password: str):
    conn = create_conn()
    # Cerco l'utente con la mail scritta nel login
    rs = conn.execute(Select([db_init.users.c.password]).where(
        db_init.users.c.email == email))
    real_pwd = None
    fetch = rs.fetchone()
    if fetch is not None:
        # Estraggo la password
        real_pwd = fetch['password']
    conn.close()
    # Controllo che hash e password coincidano
    if (real_pwd and check_password_hash(real_pwd, password)):
        user = user_by_email(email)
        # Effettuo il login
        login_user(user)
        return True
    return False


# Aggiorna la password per l'utente associato a idUser
def change_password(idUser: int, passwordForm):
    conn = create_conn()
    rs = conn.execute(Select([db_init.users.c.password]).where(
        db_init.users.c.id == idUser))
    # Controllo che la vecchia password inserita sia corretta
    oldPasswordCheck = check_password_hash(
        rs.fetchone()['password'], passwordForm['oldPassword'])
    # Se la vecchia password è corretta e quella nuova rispetta le policy di sicurezza aggiorno l'utente con la sua nuova password
    if oldPasswordCheck & password_check(passwordForm['newPassword']):
        update_conn(conn, "READ COMMITTED")
        # noqa pylint: disable=no-value-for-parameter
        conn.execute(db_init.users.update().where(db_init.users.c.id ==
                                                  idUser).values(password=generate_password_hash(passwordForm['newPassword'])))
        conn.close()
    elif not oldPasswordCheck:
        flash("Vecchia password sbagliata", "pass-error")
        conn.close()
    else:
        flash("La password deve avere almeno 5 caratteri ed una cifra", "pass-error")
        conn.close()
