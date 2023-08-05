
class Ticket:
    # noqa pylint: disable=redefined-builtin,too-many-arguments
    def __init__(self, id, date, idUser, idShow, idSeat, price):
        """Inizializza un biglietto."""
        super().__init__()
        self.id = id
        self.date = date
        self.idUser = idUser
        self.idShow = idShow
        self.idSeat = idSeat
        self.price = price

    def get_id(self):
        return (self.id)


class TicketDetail:
    # noqa pylint: disable=redefined-builtin,too-many-arguments
    def __init__(self, id, filmName, date, price, showDate, theater, seat):
        """Inizializza i dettagli di un biglietto."""
        super().__init__()
        self.id = id
        self.filmName = filmName
        self.date = date
        self.price = price
        self.showDate = showDate
        self.theater = theater
        self.seat = seat

    def get_id(self):
        return (self.id)
