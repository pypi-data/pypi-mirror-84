import pytest
from server_requests.login import check_credentials
from server_requests.films import film_by_id
from models.film import Genre
from app import app
from flask import current_app

def test_nothing():
    assert(True)
