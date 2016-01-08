
class TicTacToeException(Exception):
    pass

class TicTacToeBoardException(TicTacToeException):
    pass

class InvalidCellNumber(TicTacToeBoardException):
    pass

class InvalidTotalMoves(TicTacToeBoardException):
    pass

class UnknownCellOwner(TicTacToeBoardException):
    pass

class CellIsTaken(TicTacToeBoardException):
    pass

class InvalidPlayer(TicTacToeBoardException):
    pass

class InvalidBinary(TicTacToeException):
    pass

class InvalidCell(TicTacToeException):
    pass
class InvalidGrid(TicTacToeException):
    pass
class IncompatibleGrid(TicTacToeException):
    pass

class InvalidMove(TicTacToeException):
    pass
class InvalidHash(TicTacToeException):
    pass
class InvalidBinaryMode(TicTacToeException):
    pass
class InvalidHashMode(TicTacToeException):
    pass

class InvalidLine(TicTacToeException):
    pass
