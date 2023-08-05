from db import create_conn
from models.user import User
import db_init
from models.user import Roles
from sqlalchemy.sql import Select, func


# Trova un utente cercandolo per email e lo ritorna
def user_by_email(email):
    conn = create_conn()
    rs = conn.execute(Select([db_init.users]).where(
        db_init.users.c.email == email))
    user = rs.fetchone()
    conn.close()
    return User(user.email, user.password, user.role, user.firstName, user.lastName, user.id)


# Ottieni il numero totale di clienti
def get_n_clients():
    conn = create_conn()
    rs = conn.execute(Select([func.count()]).select_from(
        db_init.users).where(db_init.users.c.role == Roles.CLIENT))
    n_users = rs.fetchall()
    conn.close()
    # Siccome ottengo una tupla dentro una lista devo tirare fuori il vero numero
    n_users = (n_users[0])[0]
    return n_users
