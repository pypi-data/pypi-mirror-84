import db_init
from db import create_conn, update_conn
from models.theater import Theater
from sqlalchemy.sql import Select


# Inserisci una nuova sala cinematografica
def insert_theater(theater: Theater) -> Theater:
    # noqa pylint: disable=no-value-for-parameter
    ins = db_init.theaters.insert()
    conn = create_conn()
    existingTheater = conn.execute(Select([db_init.theaters.c.id]).where(
        db_init.theaters.c.name == theater.name)).fetchone()
    if existingTheater is None:
        update_conn(conn, "READ COMMITTED")
        conn.execute(ins, [
            {'name': theater.name}
        ])
        conn.close()
        return theater
    conn.close()
    return None


# Ottieni l'elenco delle sale
def get_theaters():
    conn = create_conn()
    rs = conn.execute(Select([db_init.theaters]))
    theaters = rs.fetchall()
    conn.close()
    return theaters
