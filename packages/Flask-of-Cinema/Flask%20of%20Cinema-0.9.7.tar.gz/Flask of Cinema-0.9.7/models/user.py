from enum import Enum
from flask_login import UserMixin


class User(UserMixin):
    # noqa pylint: disable=redefined-builtin,too-many-arguments
    def __init__(self, email, password, role, firstName, lastName, id=None):
        """Inizializza un utente."""
        super().__init__()
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.role = role

    def get_id(self):
        return (self.id)


class Roles(Enum):
    CLIENT = 'Client'
    MANAGER = 'Manager'
