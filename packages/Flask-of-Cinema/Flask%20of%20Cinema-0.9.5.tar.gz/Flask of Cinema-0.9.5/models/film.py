from enum import Enum


class Film:
    # noqa pylint: disable=redefined-builtin
    def __init__(self, id, name, genre, year):
        """Inizializza un film."""
        super().__init__()
        self.id = id
        self.name = name
        self.year = year
        self.genre = genre

    def get_id(self):
        return (self.id)


class Genre(Enum):
    HORROR = 'Horror'
    FANTASY = 'Fantasy'
