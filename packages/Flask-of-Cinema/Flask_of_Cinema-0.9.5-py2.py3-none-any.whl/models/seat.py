
class Seat:
    # noqa pylint: disable=redefined-builtin
    def __init__(self, id, name, idTheater):
        """Inizializza un posto a sedere."""
        super().__init__()
        self.id = id
        self.name = name
        self.idTheater = idTheater

    def get_id(self):
        return (self.id)


class SeatOccupied:
    # noqa pylint: disable=redefined-builtin
    def __init__(self, id, name, isOccupied):
        """Inizializza un posto a sedere occupato."""
        super().__init__()
        self.id = id
        self.name = name
        self.isOccupied = isOccupied

    def get_id(self):
        return (self.id)
