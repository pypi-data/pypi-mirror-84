from db import create_conn, update_conn
from sqlalchemy.sql import Select, desc, case
from models.ticket import TicketDetail
import db_init
from datetime import datetime
from typing import List


# Inserisce un biglietto per posto selezionato nella form di acquisto dei biglietti
def insert_all_tickets(tickets_form, current_user_id) -> bool:
    # Recupero tutti i posti selezionati
    # noqa pylint: disable=unnecessary-lambda 
    tickets_seats = list(map(lambda seat: int(seat),
                             tickets_form.getlist('seats[]')))
    price = float(tickets_form.get('price'))
    show_id = int(tickets_form.get('idShow'))
    conn = create_conn()
    # Controllo che non siano già stati acquistati dei biglietti coi posti selezionati in un'altra sessione
    existingOccupiedSeats = conn.execute(Select([db_init.tickets.c.idSeat]).where(
        (db_init.tickets.c.idShow == show_id) &
        db_init.tickets.c.idSeat.in_(tickets_seats))).fetchone()
    # Se i posti sono tutti liberi inserisco i posti
    if existingOccupiedSeats is None:
        # noqa pylint: disable=no-value-for-parameter
        ins = db_init.tickets.insert()
        update_conn(conn, "READ COMMITTED")
        # Per ogni posto selezionato creo un biglietto
        for seat in tickets_seats:
            conn.execute(ins, [
                {'idUser': current_user_id,
                 'idShow': show_id, 'idSeat': seat, 'date': datetime.now(), 'price': price}
            ])
        conn.close()
        return True

    conn.close()
    return False


# Prende la lista dei biglietti di un utente con una colonna isDeletable che mi dice se il biglietto può essere cancellato:
# ovvero se lo spettacolo non è ancora iniziato
def get_tickets(idUser) -> List[TicketDetail]:
    conn = create_conn()
    rs = conn.execute(
        Select([db_init.tickets.c.id, db_init.films.c.name.label('filmName'),
                db_init.tickets.c.date, db_init.tickets.c.price, db_init.shows.c.date.label(
                    'showDate'),
                db_init.theaters.c.name.label('theater'), db_init.seats.c.name.label('seat'), case(
                    [
                        (db_init.shows.c.date > datetime.now(), True)
                    ],
                    else_=False
        ).label('isDeletable')])
        .select_from(db_init.tickets
                     .join(
                         db_init.shows, db_init.tickets.c.idShow == db_init.shows.c.id)
                     .join(db_init.films, db_init.films.c.id == db_init.shows.c.idFilm)
                     .join(db_init.seats, db_init.tickets.c.idSeat == db_init.seats.c.id)
                     .join(db_init.theaters, db_init.shows.c.idTheater == db_init.theaters.c.id)
                     ).where(idUser == db_init.tickets.c.idUser).order_by(desc(db_init.tickets.c.date)))
    tickets_res = rs.fetchall()
    conn.close()
    return tickets_res


# Cancella un biglietto tramite id
def delete_ticket(idTicket: int):
    conn = create_conn()
    # noqa pylint: disable=no-value-for-parameter
    conn.execute(db_init.tickets.delete().where(
        (db_init.tickets.c.id == idTicket) & (db_init.tickets.c.idShow == db_init.shows.c.id) & (db_init.shows.c.date > datetime.now())))
    conn.close()
