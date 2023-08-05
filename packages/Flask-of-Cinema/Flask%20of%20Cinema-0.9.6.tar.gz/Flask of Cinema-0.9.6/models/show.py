class Show:
    # noqa pylint: disable=redefined-builtin,too-many-arguments
    def __init__(self, id, idTheater, date, idFilm, price):
        """Inizializza uno show."""
        super().__init__()
        self.id = id
        self.idTheater = idTheater
        self.idFilm = idFilm
        self.date = date
        self.price = price

    def get_id(self):
        return (self.id)


class ShowDetail:
    # noqa pylint: disable=redefined-builtin,too-many-arguments
    def __init__(self, id, filmName, theaterName, date, price, idFilm=None, idTheater=None):
        """Inizializza i dettagli di uno show."""
        super().__init__()
        self.id = id
        self.filmName = filmName
        self.theaterName = theaterName
        self.date = date
        self.price = price
        self.idFilm = idFilm
        self.idTheater = idTheater
