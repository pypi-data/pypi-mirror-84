import db_init
from db import create_conn, update_conn
from models.film import Film
from models.show import Show
from models.film_shows import FilmShows
from sqlalchemy.sql import Select, case
from sqlalchemy import and_
from datetime import date, datetime, timedelta
from typing import List


# Permette di inserire un nuovo film o di effettuare l'update
# di uno pre-esistente a seconda che il film esista già oppure no
def insert_film(film: Film) -> Film:
    conn = create_conn()
    # Controllo che il film non sia già nel db
    existingFilm = conn.execute(Select([db_init.films.c.id]).where(
        db_init.films.c.id == film.id)).fetchone()
    if existingFilm is None:
        # Inserisco il nuovo film
        # noqa pylint: disable=no-value-for-parameter
        ins = db_init.films.insert()
        update_conn(conn, "READ COMMITTED")
        conn.execute(ins, [
            {'name': film.name,
                'genre': film.genre, 'year': film.year}
        ])
        conn.close()
        return film

    # Se il film esiste già eseguo l'update
    update_conn(conn, "READ COMMITTED")
    # noqa pylint: disable=no-value-for-parameter
    conn.execute(db_init.films.update().where(db_init.films.c.id == film.id).values(
        name=film.name, genre=film.genre, year=film.year))
    conn.close()
    return film


# Esegue una semplice query per prendere un film tramite il suo id
# noqa pylint: disable=redefined-builtin
def film_by_id(id) -> Film:
    conn = create_conn()
    rs = conn.execute(Select([db_init.films]).where(
        db_init.films.c.id == id))
    film = rs.fetchone()
    conn.close()
    return Film(film.id, film.name, film.genre, film.year)


# Prende la lista dei film filtrandoli per genere e titolo se impostati
def film_by_genre_and_title(genre: str, title: str):
    conn = create_conn()
    # Controllo che si stia filtrando per genere. In tal caso salvo il confronto, se no lo valorizzo a True
    # (per non farlo valere nell'and della where)
    cond1 = True if genre is None else (db_init.films.c.genre == genre.upper())
    # Controllo che si stia filtrando per nome. In tal caso salvo il confronto (un like sul title), se no lo valorizzo a True
    # (per non farlo valere nell'and della where)
    cond2 = True if title is None else (
        db_init.films.c.name.ilike('%' + title + '%'))
    # Select di tutte le colonne della tabella film e una colonna isDeletable per controllare se il film è cancellabile
    # (ovvero se non è ancora stato proiettato in passato)
    # film filtrati rispetto a nome e genere e ordinati in ordine alfabetico
    rs = conn.execute(Select([db_init.films, case(
        [
            (db_init.films.c.id.in_(Select([db_init.shows.c.idFilm])), False)
        ],
        else_=True
    ).label('isDeletable')]).where(and_(cond1, cond2)).order_by(db_init.films.c.name))
    films = rs.fetchall()
    conn.close()
    return films


# Ritorna una lista di film con al suo interno oltre a delle informazioni su di esso, anche la lista di proiezione
# del film stesso. Serve per mostrare la lista delle proiezioni ai clienti
def get_film_with_shows(date_shows: str):
    # Prendo la data passata, se non c'è setto quella di oggi
    if date_shows and (len(date_shows) > 0):
        date_shows = datetime.strptime(date_shows, "%Y-%m-%d")
    else:
        date_shows = datetime.strptime(
            date.today().strftime('%Y-%m-%d'), '%Y-%m-%d')
    conn = create_conn()
    # Select di tutte le colonne di films e di show in join
    # filtrate per tutti gli show compresi tra la data selezionata e
    # l'inizio del giorno successivo (quindi della data selezionata)
    rs = conn.execute(Select([db_init.films, db_init.shows]).where(
        (db_init.films.c.id == db_init.shows.c.idFilm) & (
            (db_init.shows.c.date >= date_shows) & (db_init.shows.c.date < (date_shows + timedelta(days=1))))
    ).order_by(db_init.films.c.name, db_init.shows.c.date))
    result = rs.fetchall()
    films: List[FilmShows] = []
    # Prendo tutte le tuple risultanti e le ciclo per creare una lista di film che a loro volta al loro interno hanno una
    # lista di proiezioni che gli appartengono
    for show in result:
        film = next((x for x in films if x.film.id == show.idFilm), None)
        if film:
            film.addShow(Show(show[4], show[5],
                              show[7], show[6], show[8]))
        else:
            firstFilm = FilmShows(date_shows, Film(
                show[0], show[1], show[2], show[3]))
            films.append(firstFilm)
            firstFilm.addShow(Show(show[4], show[5],
                                   show[7], show[6], show[8]))
    conn.close()
    return films


# Elimina un film by id
def delete_film(idFilm: int):
    conn = create_conn()
    # Se non esistono ancora show per un determinato film posso eliminarlo
    existingShow = conn.execute(Select([db_init.shows.c.id]).where(
        db_init.shows.c.idFilm == idFilm)).fetchone()
    if existingShow is None:
        # noqa pylint: disable=no-value-for-parameter
        conn.execute(db_init.films.delete().where(
            (db_init.films.c.id == idFilm)
        ))
    conn.close()
