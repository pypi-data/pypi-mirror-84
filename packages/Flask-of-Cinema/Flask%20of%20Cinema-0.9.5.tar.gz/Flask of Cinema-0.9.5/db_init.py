import server_requests.films
import server_requests.registration
import server_requests.seats
import server_requests.theatre
from db import engine
from models.film import Film, Genre
from models.seat import Seat
from models.theater import Theater
from models.user import Roles
from sqlalchemy import (Column, DateTime, Float, ForeignKey,
                        Integer, MetaData, String, Table,
                        UniqueConstraint, event)
from sqlalchemy.types import Enum

# Aggiungere qui tutti i metadati necessari per l'inizializzazione
metadata = MetaData()

# Create metadata for the database
# Tabella degli utenti
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('email', String, nullable=False),
              Column('firstName', String, nullable=False),
              Column('lastName', String, nullable=False),
              #   Enum mi permette di fare un check in modo tale che il ruolo assegnato faccia parte solo dei ruoli realmente esistenti,
              #   viene utilizzato un Enum nativo del backend se disponibile oppure un CHECK
              Column('role', Enum(Roles), nullable=False),
              Column('password', String, nullable=False),

              UniqueConstraint('email')
              )

# Tabella per i film disponibili all'interno del cinema
films = Table('films', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('genre', Enum(Genre)),
              Column('year', Integer),

              UniqueConstraint('name', 'year')
              )

# Tabella dei biglietti acquistati
tickets = Table('tickets', metadata,
                Column('id', Integer, primary_key=True),
                Column('idUser', Integer,
                       ForeignKey('users.id'),
                       nullable=False
                       ),
                Column('date', DateTime, nullable=False),
                Column('idShow', Integer,
                       ForeignKey('shows.id'),
                       nullable=False
                       ),
                Column('idSeat', Integer,
                       ForeignKey('seats.id'),
                       nullable=False
                       ),
                Column('price', Float, nullable=False)
                )

# Tabella delle proiezioni
shows = Table('shows', metadata,
              Column('id', Integer, primary_key=True),
              Column('idTheater', Integer,
                     ForeignKey('theaters.id'),
                     nullable=False
                     ),
              Column('idFilm', Integer,
                     ForeignKey('films.id'),
                     nullable=False
                     ),
              Column('date', DateTime, nullable=False),
              Column('price', Float, nullable=False)
              )

# Tabella delle sale del cinema
theaters = Table('theaters', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('name', String)
                 )

# Tabella dei posti "occupati", ovvero quelli selezionati in fase di acquisto e non ancora acquistati
occupied_seats = Table('occupied_seats', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('idUser', Integer,
                              ForeignKey('users.id'),
                              nullable=False
                              ),
                       Column('idSeat', Integer,
                              ForeignKey('seats.id'), nullable=False),
                       Column('creationTime', DateTime,  nullable=False),
                       Column('idShow', Integer,
                              ForeignKey('shows.id'),
                              nullable=False
                              )
                       )

# Tabella dei posti disponibili all'interno del cinema
seats = Table('seats', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String, nullable=False),
              Column('idTheater', Integer,
                     ForeignKey('theaters.id'),
                     nullable=False
                     )
              )


# Crea dei film di default alla creazione della tabella film
@event.listens_for(films, 'after_create')
# noqa pylint: disable=unused-argument
def create_films(*args, **kwargs):
    server_requests.films.insert_film(
        Film(None, 'Harry Potter', Genre.FANTASY, '1997'))
    server_requests.films.insert_film(
        Film(None, 'Narnia', Genre.FANTASY, '2005'))
    server_requests.films.insert_film(
        Film(None, 'Saw', Genre.HORROR, '2004'))
    server_requests.films.insert_film(
        Film(None, 'Final Destination', Genre.HORROR, '2000'))


# Crea le sale del cinema alla creazione della tabella theaters
@event.listens_for(theaters, 'after_create')
# noqa pylint: disable=unused-argument
def create_theaters(*args, **kwargs):
    server_requests.theatre.insert_theater(Theater(None, 'Sala 1'))
    server_requests.theatre.insert_theater(Theater(None, 'Sala 2'))


# Creazione automatica dei posti alla creazione della tabella seats
@event.listens_for(seats, 'after_create')
# noqa pylint: disable=unused-argument
def create_seats(*args, **kwargs):
    # Creo dei nomi (A1...A10, B1...B10) per i posti
    for i in range(0, 50):
        name = (chr(65 + int(i // 10)) + str((i % 10) + 1))
        server_requests.seats.insert_seat(
            Seat(i + 1, name, 1))
        server_requests.seats.insert_seat(
            Seat(i + 51, name, 2))


# Creazione di un utente admin e un client alla creazione della tabella users
@event.listens_for(users, 'after_create')
# noqa pylint: disable=unused-argument
def create_users(*args, **kwargs):
    server_requests.registration.insert_user(
        {'email': 'jack@gmail.com', 'password': 'manager1', 'role': Roles.MANAGER, 'firstName': 'Jack', 'lastName': 'Jones'})
    server_requests.registration.insert_user(
        {'email': 'wendy@gmail.com', 'password': 'client1', 'role': Roles.CLIENT, 'firstName': 'Wendy', 'lastName': 'Williams'})


metadata.create_all(engine)
