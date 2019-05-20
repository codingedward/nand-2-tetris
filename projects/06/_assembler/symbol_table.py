import sys

class SymbolTable:
    def __init__(self):
        self.clear()

    def clear(self):
        self._table = {}

    def add_entry(self, symbol, address):
        self._table[symbol] = address

    def contains(self, symbol):
        return symbol in self._table

    def get_address(self, symbol):
        if not self.contains(symbol):
            sys.stderr.write('[SymbolTable]: Table does not contain symbol: %s' % symbol)
            sys.exit(1)
        return self._table[symbol]
