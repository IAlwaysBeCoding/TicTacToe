
import weakref

from tictactoe.hash.cell import Cell, create_and_verify_cell
from tictactoe.settings  import TTT_3_IN_A_ROW, TTT_4_IN_A_ROW, TTT_5_IN_A_ROW

class Move(Cell):

    _Refs   = weakref.WeakValueDictionary()
    _Hashes = weakref.WeakValueDictionary()

    MODE    = TTT_3_IN_A_ROW

    def __new__(cls,number,player):
        return create_and_verify_cell(number=number,
                                      player=player,
                                      cell_class=cls)

    @classmethod
    def from_hash(cls,hash):
        previous_move = cls._Hashes.get(hash,None)
        return previous_move if previous_move else super(Move,cls).from_hash(hash=hash)


class Move4(Cell):

    _Refs   = weakref.WeakValueDictionary()
    _Hashes = weakref.WeakValueDictionary()

    MODE    = TTT_4_IN_A_ROW

    def __new__(cls,number,player):
        return create_and_verify_cell(number=number,
                                      player=player,
                                      cell_class=cls)

    @classmethod
    def from_hash(cls,hash):
        previous_move = cls._Hashes.get(hash,None)
        return previous_move if previous_move else super(Move4,cls).from_hash(hash=hash)


class Move5(Cell):

    _Refs   = weakref.WeakValueDictionary()
    _Hashes = weakref.WeakValueDictionary()

    MODE    = TTT_5_IN_A_ROW

    def __new__(cls,number,player):
        return create_and_verify_cell(number=number,
                                      player=player,
                                      cell_class=cls)

    @classmethod
    def from_hash(cls,hash):
        previous_move = cls._Hashes.get(hash,None)
        return previous_move if previous_move else super(Move5,cls).from_hash(hash=hash)



