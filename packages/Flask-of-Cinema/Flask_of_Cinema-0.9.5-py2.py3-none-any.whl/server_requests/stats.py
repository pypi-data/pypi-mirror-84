from db import create_conn
from sqlalchemy.sql import Select, func, desc
import db_init
from models.user import Roles


# Ottieni il numero di tickets venduti
def get_n_tickets():
    conn = create_conn()
    tickets_table = db_init.tickets
    rs = conn.execute(Select([func.count()]).select_from(tickets_table))
    conn.close()
    n_tickets = rs.fetchone()[0]
    return n_tickets


# Ottieni i profitti totali
def get_profits():
    conn = create_conn()
    tickets_table = db_init.tickets
    rs = conn.execute(Select([func.sum(tickets_table.c.price)]))
    conn.close()
    profits = rs.fetchone()[0]
    return profits


# Ottieni i 5 clienti che hanno speso più soldi in totale
def get_best_clients():
    conn = create_conn()
    # coalesce prende il primo valore non nullo di una lista (se è nulla la somma prende 0)
    rs = conn.execute(Select([db_init.users.c.email, func.coalesce(func.sum(db_init.tickets.c.price), 0).label('totalMoney'),
                              func.count(db_init.tickets.c.id).label('totalTickets')]).select_from(
        db_init.users.outerjoin(
            db_init.tickets, db_init.users.c.id == db_init.tickets.c.idUser)
    )
        .where(db_init.users.c.role == Roles.CLIENT)
        .group_by(db_init.users.c.id).order_by(desc('totalMoney')))
    users = rs.fetchall()
    conn.close()
    users = users[0:5]
    return users


# Ottieni i 5 film che hanno venduto più biglietti
def get_popular_films():
    conn = create_conn()
    rs = conn.execute(Select([db_init.films.c.name, func.count(db_init.tickets.c.id).label('totalTickets')]).select_from(
        db_init.films
        .outerjoin(db_init.shows, db_init.films.c.id == db_init.shows.c.idFilm)
        .outerjoin(db_init.tickets, db_init.shows.c.id == db_init.tickets.c.idShow)
    ).group_by(db_init.films.c.id).order_by(desc('totalTickets')))
    films = rs.fetchall()
    conn.close()
    films = films[0:5]
    return films
