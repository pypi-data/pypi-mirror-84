import db_init
from datetime import datetime, timedelta
from db import create_conn, update_conn
from sqlalchemy.sql import Select, case
from sqlalchemy import desc


# Prende una proiezione by id e ritorna con alcune informazioni in più (nome film, nome sala ecc.)
def get_show_by_id(showId: int):
    conn = create_conn()
    rs = conn.execute(Select([db_init.shows.c.date, db_init.shows.c.price, db_init.films.c.name.label("filmName"),
                              db_init.theaters.c.name.label(
                                  "theaterName"), db_init.shows.c.id,
                              db_init.films.c.id.label("idFilm"), db_init.theaters.c.id.label("idTheater")]).where(
        (db_init.shows.c.idTheater == db_init.theaters.c.id) & (
            db_init.shows.c.idFilm == db_init.films.c.id) & (showId == db_init.shows.c.id)
    ))
    show = rs.fetchone()
    conn.close()
    return show


# Prende tutte le proiezioni filtrandole per un lasso di tempo e per un determinato film
# Inoltre ritorna una colonna isDeletable che mi dice se lo show si può eliminare,
# ovvero se quella proiezione non è ancora avvenuta
def get_shows(start_date: str, end_date: str, film_id: int):
    conn = create_conn()
    rs = conn.execute(Select([db_init.shows.c.date, db_init.shows.c.price, db_init.films.c.name.label("filmName"),
                              db_init.theaters.c.name.label("theaterName"), db_init.shows.c.id, case(
        [
            (db_init.shows.c.date > datetime.now(), True)
        ],
        else_=False
    ).label('isDeletable')]).where(
        check_filters(start_date, end_date, film_id) & (
            db_init.shows.c.idTheater == db_init.theaters.c.id)
        & (db_init.shows.c.idFilm == db_init.films.c.id)).order_by(
        desc(db_init.shows.c.date)
    ))
    shows = rs.fetchall()
    conn.close()
    return shows


# Utilizzato in get show per filtrare per date e film id la lista di proiezioni
def check_filters(start_date: str, end_date: str, film_id: int):
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    if not start_date and not end_date:
        return check_film_id(film_id)
    if start_date and not end_date:
        return (db_init.shows.c.date > start_date) & (db_init.films.c.id == film_id & check_film_id(film_id))
    if end_date and not start_date:
        return (db_init.shows.c.date < end_date) & check_film_id(film_id)
    return (db_init.shows.c.date > start_date) & ((db_init.shows.c.date <= end_date) & check_film_id(film_id))


# Controlla che esista il film id in caso ritorna True perchè non sto filtrando per id
def check_film_id(film_id: int):
    if(film_id):
        return (db_init.films.c.id == film_id)
    return True


# Inserisce tutte le proiezioni create nel form.
def insert_show(show_form, id_film):
    if(not show_form.get('date_start') or not show_form.get('date_end')):
        return False
    days = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
    # noqa pylint: disable=no-value-for-parameter
    ins = db_init.shows.insert()
    date_start = datetime.strptime(show_form.get('date_start'), "%Y-%m-%d")
    date_end = datetime.strptime(show_form.get('date_end'), "%Y-%m-%d")
    # Differenza tra la data di inizio e la data di fine
    delta = date_end - date_start
    # Per ogni giorno dalla data di inizio alla data di fine...
    conn = create_conn()
    for i in range(delta.days + 1):
        day = date_start + timedelta(days=i)
        week_day = days[day.weekday()]
        hours = show_form.getlist(week_day+'-hour[]')
        theaters = show_form.getlist(week_day+'-theater[]')
        # Per ogni ora (ovvero per ogni form con ora e sala nel giorno corrente)
        # noqa pylint: disable=consider-using-enumerate
        for i in range(len(hours)):
            # Creo il datetime dalla data e dall'ora
            day = datetime.combine(
                day, datetime.strptime(hours[i], '%H:%M').time())
            # Prendo la sala della proiezione
            theater = theaters[i]
            # Controllo che lo show non esista già
            existingShow = conn.execute(Select([db_init.shows.c.date]).where(
                (db_init.shows.c.date == day) & (db_init.shows.c.idTheater == theater))).fetchone()
            # Se non esiste aggiungi la nuova proiezione
            if existingShow is None:
                update_conn(conn, "READ COMMITTED")
                conn.execute(ins, [
                    {
                        'idTheater': theater,
                        'idFilm': id_film,
                        'date': day,
                        'price': show_form.get('price')
                    }
                ])
    conn.close()
    return True


# Elimina lo show
def delete_show(idShow: int):
    conn = create_conn()
    # noqa pylint: disable=no-value-for-parameter
    conn.execute(db_init.shows.delete().where(
        (db_init.shows.c.id == idShow) & (db_init.shows.c.date > datetime.now())))
    conn.close()
