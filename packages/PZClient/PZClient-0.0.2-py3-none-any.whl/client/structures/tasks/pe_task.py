class PeMessage:
    def __init__(self, symbol: str):
        self._symbol = symbol.lower()

    @property
    def symbol(self):
        return self._symbol
