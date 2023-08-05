import pytest
from server_requests.login import check_credentials
from server_requests.films import film_by_id
from models.film import Genre
from app import app
from flask import current_app

def test_nothing():
    assert(True)

def test_user():
    with app.app_context():
        with current_app.test_request_context():
            email='wendy@gmail.com'
            password='client1'
            assert(True == check_credentials(email, password))

def test_film():
    id = 1
    Film = film_by_id(id)
    assert(Film.name=='Harry Potter')       
    assert(Film.genre==Genre.FANTASY)
    assert(Film.year==1997)