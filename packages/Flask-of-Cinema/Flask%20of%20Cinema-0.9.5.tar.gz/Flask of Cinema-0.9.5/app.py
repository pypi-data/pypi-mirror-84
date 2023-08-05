from datetime import date, datetime, timedelta
from os import getenv

from db import create_conn
from db_init import users
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
from flask.helpers import flash
from flask_login import LoginManager, current_user, login_required, logout_user
from models.film import Film, Genre
from models.user import Roles, User
from server_requests.films import (delete_film, film_by_genre_and_title,
                                   film_by_id, get_film_with_shows,
                                   insert_film)
from server_requests.login import change_password, check_credentials
from server_requests.registration import insert_user
from server_requests.seats import add_occupied_seats as add_occ_seats
from server_requests.seats import get_seats_occupied
from server_requests.seats import remove_occupied_seats as remove_occ_seats
from server_requests.shows import (delete_show, get_show_by_id, get_shows,
                                   insert_show)
from server_requests.stats import (get_best_clients, get_n_tickets,
                                   get_popular_films, get_profits)
from server_requests.theatre import get_theaters
from server_requests.tickets import (delete_ticket, get_tickets,
                                     insert_all_tickets)
from server_requests.users import get_n_clients
from sqlalchemy.sql import Select
from utils.role_required_decorator import role_required

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = getenv("FLASK_SECRET_KEY")
login_manager = LoginManager(app)
login_manager.init_app(app)


# Globalizzo Roles per utilizzarlo nel template
@app.context_processor
def get_current_user():
    return {"Roles": Roles}


# Controlla ad ogni chiamata lo stato della sessione.
# Se sono passati 5 minuti tra una chiamata e l'altra la sessione è scaduta ed esegue il logout
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
    session.modified = True


# Recupera l'utente loggato
@login_manager.user_loader
def load_user(user_id: int):
    conn = create_conn()
    rs = conn.execute(Select([users]).where(
        users.c.id == user_id))
    user = rs.fetchone()
    conn.close()
    return User(user.email, user.password, user.role, user.firstName, user.lastName, user.id)


# Route verso la home. Controlla se sei autenticato.
# Se sei autenticato ti rimanda alla pagina dedicata al tuo ruolo (client o manager)
# Se non sei autenticato torni alla login
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for(current_user.role.value.lower()))
    return render_template('login.html')


# Route verso la home del manager
# Porta alla home del manager
@app.route("/manager")
@role_required(Roles.MANAGER)
def manager():
    return render_template('home-gestore.html')


# Route verso la home del client
# Qui viene mostrata la lista degli spettacoli filtrata per la data selezionata
@app.route("/client", methods=['GET', 'POST'])
@role_required(Roles.CLIENT)
def client():
    filter_date = datetime.strptime(request.args.get(
        'date'), '%Y-%m-%d') if request.args.get('date') else date.today()
    return render_template('home-cliente.html', films=get_film_with_shows(request.args.get('date')), date=filter_date, now=datetime.now())


# Route verso login
# La pagina di accesso
# POST: riceve email e password, le controlla, se corrette rimanda in home
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        result = check_credentials(
            request.form['email'], request.form['password'])
        if not result:
            flash("Username o password errati")
        return redirect(url_for('home'))
    return redirect(url_for('home'))


# Chiamando questo endpoint esegue il logout di flask_login
@app.route('/logout')
def logout():
    logout_user()  # chiamata a flask - login
    return redirect(url_for('home'))


# Route verso la registrazione
# Mostra la pagina di registrazione di un cliente
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Inserisce un nuovo utente con i dati del form e il ruolo cliente
        if insert_user({**request.form, **{'role': Roles.CLIENT}}) is not None:
            return redirect(url_for('login'))
        return render_template('registration.html', regForm=request.form)
    return render_template('registration.html', regForm=request.form)


# Chiamata per aggiornare i dati dell'utente (email, nome e cognome)
# referrer è l'url alla chiamata precedente
# (change-password può essere chiamato da tutte le pagine quindi deve tornare all'ultima pagina aperta)
@app.route('/update-user', methods=['POST'])
@login_required
def update_user_endpoint():
    insert_user(request.form, current_user.email)
    return redirect(request.referrer)


# Chiamata per aggiornare la password dell'utente.
# referrer è l'url alla chiamata precedente
# (change-password può essere chiamato da tutte le pagine quindi deve tornare all'ultima pagina aperta)
@app.route('/change-password', methods=['POST'])
@login_required
def change_password_endpoint():
    change_password(current_user.id, request.form)
    return redirect(request.referrer)


# Route verso i film
# Mostra la lista dei film disponibili,
# oppure passando un id mostra il form di modifica (anche con valore None, in quel caso mostra il form di creazione).
@app.route("/films", methods=['GET', 'POST'])
@role_required(Roles.MANAGER)
def films_endpoint():
    if request.method == 'POST':
        # Inserisce un nuovo film nel caso l'id è None, se no esegue l'update del film con id == request.form["id"]
        insert_film(Film(None if request.form["id"] == 'None' else int(request.form["id"]), request.form["name"],
                         request.form["genre"], request.form["year"]))
        return redirect(url_for('films_endpoint'))

    if request.args.get('idFilm'):
        # Se alla richiesta passo l'argomento idFilm apre il form di modifica o creazione (a seconda che sia None o un numero)
        return render_template('films.html',
                                filmForm=True if request.args.get('idFilm') == 'None' else film_by_id(
                                    int(request.args.get('idFilm'))),
                                genres=list(e.name for e in Genre))

    # Se non passo nessun argomento alla richiesta mostro la lista dei film disponibili
    return render_template('films.html',
                            films=film_by_genre_and_title(request.args.get(
                                'genre'), request.args.get('title')),
                            role=current_user.role.name,
                            genres=list(e.name for e in Genre))


# Chiamata per eliminare un film
@app.route("/delete-film", methods=['POST'])
@role_required(Roles.MANAGER)
def delete_film_endpoint():
    delete_film(int(request.form.get('id')))
    return redirect(url_for('films_endpoint'))


# Chiamata ai tickets
# Con idShow: Mostra la pagina di acquisto di un biglietto per lo show rappresentato da id Show
# Senza idShow:
#   - GET: Ti mostra una pagina con tutti i biglietti acquistati dal cliente corrente
#   - POST: Inserisce tutti i biglietti acquistati (uno per posto a sedere selezionato)
@app.route("/tickets/<idShow>", methods=['GET'])
@app.route("/tickets", methods=['GET', 'POST'])
@role_required(Roles.CLIENT)
def tickets_endpoint(idShow=None):
    if request.method == 'POST':
        # Prova ad inserire i biglietti selezionati
        if insert_all_tickets(request.form, current_user.id):
            return redirect(url_for('tickets_endpoint'))
        # Se non ci riesce significa che qualcuno li ha già acquistati: ricarico la lista di posti disponibili
        flash('Qualcuno ha acquistato il biglietto per uno o più dei posti che hai selezionato. Ecco la lista aggiornata.', 'seats-error')
        show = get_show_by_id(int(request.form['idShow']))
        film = film_by_id(show.idFilm)
        return render_template('tickets.html', tickets=get_tickets(current_user.id), show=show, film=film.name, seats=get_seats_occupied(show))

    # Mostra una pagina con tutti i biglietti acquisati dall'utente attualmente connesso
    if not idShow:
        return render_template('tickets.html', tickets=get_tickets(current_user.id))
    # Mostra la pagina per acquistare i biglietti realativi allo show selezionato
    show = get_show_by_id(int(idShow))
    film = film_by_id(show.idFilm)
    return render_template('tickets.html', tickets=get_tickets(current_user.id), show=show, film=film.name, seats=get_seats_occupied(show))


# Cancella un biglietto by id
@app.route("/delete-ticket", methods=['POST'])
@role_required(Roles.CLIENT)
def delete_ticket_endpoint():
    delete_ticket(int(request.form.get('id')))
    return redirect(url_for('tickets_endpoint'))


# Route verso le proiezioni
# - POST: Crea una nuova proiezione per il film rappresentato da idFilm
# - GET: Mostra la lista delle proiezioni per un determinato film rappresentato da idFilm, opzionalmente filtrati per data
@app.route("/shows/<idFilm>", methods=['GET', 'POST'])
@role_required(Roles.MANAGER)
def shows_endpoint(idFilm):
    if request.method == 'POST':
        insert_show(request.form, idFilm)
        return redirect('/shows/'+idFilm)
    return render_template('shows.html', shows=get_shows(
        request.args.get('date_start'), request.args.get('date_end'), idFilm), film_id=idFilm,
        role=current_user.role.name, film_name=film_by_id(idFilm).name, theaters=get_theaters(),  action=request.args.get('action'))


# Cancella una proiezione by id
@app.route("/delete-show", methods=['POST'])
@role_required(Roles.MANAGER)
def delete_show_endpoint():
    delete_show(int(request.form.get('id')))
    return redirect(url_for('shows_endpoint', idFilm=request.form.get('idFilm')))


# Route verso la pagina delle statistiche
@app.route("/stats", methods=['GET'])
@role_required(Roles.MANAGER)
def stats_endpoint():
    return render_template('stats.html', n_tickets=get_n_tickets(), n_users=get_n_clients(),
                           profit=get_profits(), best_clients=get_best_clients(), popular_films=get_popular_films())


# Aggiunge un posto momentaneamente "occupato" da un client (non ancora acquistato)
@app.route("/add-occupied-seat", methods=['POST'])
@role_required(Roles.CLIENT)
def add_occupied_seats():
    return add_occ_seats(request.json['idShow'], int(request.json['idSeat']), current_user.id)


# Rimuove un posto momentaneamente "occupato" da un client (non ancora acquistato)
@app.route("/remove-occupied-seat", methods=['POST'])
@role_required(Roles.CLIENT)
def remove_occupied_seats():
    return remove_occ_seats(request.json['idShow'], int(
        request.json['idSeat']), current_user.id)
