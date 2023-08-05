class FilmShows:
    def __init__(self, date, film):
        """Inizializza uno show di un film."""
        super().__init__()
        self.date = date
        self.film = film
        self.shows = []

    def addShow(self, show):
        self.shows.append(show)
