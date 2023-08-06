
class Theater:
    # noqa pylint: disable=redefined-builtin
    def __init__(self, id, name):
        """Inizializza un teatro."""
        super().__init__()
        self.id = id
        self.name = name
        
    def get_id(self):
        return (self.id)