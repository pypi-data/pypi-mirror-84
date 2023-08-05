import db_init
from datetime import datetime, timedelta
from db import create_conn, update_conn
from models.seat import Seat
from models.show import ShowDetail
from sqlalchemy.sql import Select, case, union
from typing import List
from flask_login import current_user


# Inserisce un nuovo posto
def insert_seat(seat: Seat) -> Seat:
    # pylint: disable=no-value-for-parameter
    ins = db_init.seats.insert()
    conn = create_conn()
    existingSeat = conn.execute(Select([db_init.seats.c.id]).where(
        db_init.seats.c.id == seat.id)).fetchone()
    if existingSeat is None:
        update_conn(conn, "READ COMMITTED")
        conn.execute(ins, [
            {'id': seat.id, 'name': seat.name, 'idTheater': seat.idTheater}
        ])
        conn.close()
        return seat
    conn.close()
    return None


# Prende tutti i posti filtrati per sala
def get_seats(idTheater: int) -> List[Seat]:
    conn = create_conn()
    rs = conn.execute(Select([db_init.seats]).where(
        idTheater == db_init.seats.c.idTheater))
    seats = rs.fetchall()
    conn.close()
    return seats


# Prende tutti i posti a sedere per una determinata proiezione.
# Indica inoltre se sono già occupati da qualche altro utente oppure se sono stati selezionati
# negli ultimi 5 minuti dall'utente corrente
def get_seats_occupied(show: ShowDetail) -> List[Seat]:
    # Chiamo remove_old_occupied_seats per eliminare i vecchi posti occupati
    remove_old_occupied_seats()
    conn = create_conn()
    # Select che mi prende l'id dei posti già acquistati e quindi non più disponibili
    s1 = Select([db_init.tickets.c.idSeat.label('idSeat')]).select_from(
        (db_init.tickets.join(db_init.shows, db_init.shows.c.id == db_init.tickets.c.idShow))).where(db_init.shows.c.id == show.id)
    # Select da occupied_seats di tutti i posti occupati dagli altri utenti
    s2 = Select([db_init.occupied_seats.c.idSeat.label('idSeat')]).where(
        (db_init.occupied_seats.c.idShow == show.id) & (db_init.occupied_seats.c.idUser != current_user.id))
    # La union di s1 e s2 mi da tutti gli id dei posti occupati
    s3 = union(s1, s2)
    # Select da occupied_seats di tutti i posti che l'utente corrente ha occupato
    s4 = Select([db_init.occupied_seats.c.idSeat.label('idSeat')]).where(
        (db_init.occupied_seats.c.idShow == show.id) & (db_init.occupied_seats.c.idUser == current_user.id))
    # La query prende id e nome del posto e imposta isOccupied a True se l'id del posto è dentro s3 e a isSelected se l'id del posto è dentro s4
    rs = conn.execute(Select([db_init.seats.c.id, db_init.seats.c.name, case(
        [
            (db_init.seats.c.id.in_(s3), True)
        ],
        else_=False
    ).label('isOccupied'), case(
        [
            (db_init.seats.c.id.in_(s4), True)
        ],
        else_=False
    ).label('isSelected')]).where(db_init.seats.c.idTheater == show.idTheater))
    seats = rs.fetchall()
    conn.close()
    return seats


# Aggiunge un posto alla tabella dei posti occupati in fase d'acquisto
def add_occupied_seats(idShow: int, idSeat: int, user: int):
    # noqa pylint: disable=no-value-for-parameter
    ins = db_init.occupied_seats.insert()
    conn = create_conn()
    existingSeat = conn.execute(Select([db_init.occupied_seats.c.id]).where(
        (db_init.occupied_seats.c.idSeat == idSeat) & (db_init.occupied_seats.c.idShow == idShow))).fetchone()
    if existingSeat is None:
        update_conn(conn, "READ COMMITTED")
        conn.execute(ins, [
            {'idUser': user, 'idSeat': idSeat,
                'idShow': idShow, 'creationTime': datetime.now()}
        ])
        conn.close()
        return {'idUser': user, 'idSeat': idSeat,
                'idShow': idShow, 'creationTime': datetime.now()}
    conn.close()
    return {}


# Rimuove un posto dalla tabella dei posti occupati in fase d'acquisto
def remove_occupied_seats(idShow: int, idSeat: int, user: int):
    conn = create_conn()
    # noqa pylint: disable=no-value-for-parameter
    conn.execute(db_init.occupied_seats.delete().where((db_init.occupied_seats.c.idShow == idShow) & (
        db_init.occupied_seats.c.idSeat == idSeat) & (db_init.occupied_seats.c.idUser == user)))
    conn.close()
    return {'idUser': user, 'idSeat': idSeat,
            'idShow': idShow, 'creationTime': datetime.now()}


# Elimina tutti i posti occupati da più di 5 minuti per non avere casi di sessioni aperte con posti bloccati
def remove_old_occupied_seats():
    conn = create_conn()
    since = datetime.now() - timedelta(minutes=5)
    # noqa pylint: disable=no-value-for-parameter
    conn.execute(db_init.occupied_seats.delete().where(
        db_init.occupied_seats.c.creationTime < since))
    conn.close()
