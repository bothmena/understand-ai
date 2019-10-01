class ItemExistException(Exception):
    def __init__(self, message: str = 'you can\'t override an item that already exists', state: int = 101):
        super().__init__(message, state)
        self.message = message
        self.state = state


class ItemNotFoundException(Exception):
    def __init__(self, message: str = 'item does not exist in the state', state: int = 101):
        super().__init__(message, state)
        self.message = message
        self.state = state
