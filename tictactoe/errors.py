
class TicTacToeException(Exception):
    pass

class TicTacToeHashException(TicTacToeException):
    pass

class TicTacToeGridException(TicTacToeHashException):
    pass

class IncompatibleGrid(TicTacToeGridException):
    pass

class CellIsTaken(TicTacToeGridException):
    pass

class TicTacToeLineException(TicTacToeException):
    pass


