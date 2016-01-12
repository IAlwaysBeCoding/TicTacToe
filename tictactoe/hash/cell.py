
import weakref

from tictactoe.compute      import compute_hash
from tictactoe.errors       import InvalidHash, InvalidCell
from tictactoe.hash         import Hashable
from tictactoe.settings     import (FREE_SPACE, GAME_MODES, TTT_3_IN_A_ROW, TTT_4_IN_A_ROW,
                                    TTT_5_IN_A_ROW)
from tictactoe.verification import verify_player, verify_cell, verify_binary


def create_new_cell(cell_cls,number,player):

    cell = Hashable.__new__(cell_cls)
    cell._number = number
    cell._player = player
    cell._hash   = None
    cell._binary = None

    return cell


def create_and_verify_cell(number,player,cell_class):

    verify_player(player=player)
    verify_cell(cell=number,mode=cell_class.MODE)

    ref_key = '{}-{}'.format(number,player)
    cell = cell_class._Refs.get(ref_key,None)

    if cell is None:
        cell = create_new_cell(cell_cls=cell_class,number=number,player=player)
        cell_class._Refs[ref_key] = cell
        cell_class._Hashes[cell.hash] = cell_class._Refs[ref_key]

    return cell


class Cell(Hashable):


    _Refs   = weakref.WeakValueDictionary()
    _Hashes = weakref.WeakValueDictionary()

    MODE   = TTT_3_IN_A_ROW

    def __new__(cls,number,player=FREE_SPACE):

        return create_and_verify_cell(number=number,
                                      player=player,
                                      cell_class=cls)
    @staticmethod
    def decompose_binary(index):
        return ((index / 3) + 1, index % 3)

    @staticmethod
    def validate_binary(binary):
        if binary.count('1') != 1:
            raise InvalidCell(
                'Binary:{} is an invalid Cell. Only a single '\
                '1 can be found in the binary'.format(binary))

    @classmethod
    def from_binary(cls,binary):

        verify_binary(binary=binary,mode=GAME_MODES[cls.MODE]['GRID_STATE'])
        if isinstance(binary,(list,tuple)):
            binary = "".join([str(n) for n in binary])


        binary = "".join([b for b in reversed(binary)])

        cls.validate_binary(binary=binary)
        cell, player = cls.decompose_binary(index=binary.index('1'))

        return cls(number=cell,player=player)

    @classmethod
    def from_hash(cls,hash):
        if not isinstance(hash,(long,int)):
            raise InvalidHash('A {} type was passed to hash. Only '
                              'an long or an int type is acceptable'.format(type(hash)))

        previous_cell = cls._Hashes.get(hash,None)
        if previous_cell:
            return previous_cell
        else:
            binary = "".join([b for b in reversed(bin(hash)[2:].zfill(27))])

            cls.validate_binary(binary=binary)
            cell, player = cls.decompose_binary(index=binary.index('1'))

            return cls(number=cell,player=player)

    @property
    def hash(self):
        if self._hash is None:
            self._hash = compute_hash(cell=self.number,
                                      player=self.player,
                                      mode=self.MODE)

        return self._hash

    @hash.setter
    def hash(self,value):
        pass

    @property
    def binary(self):
        if self._binary is None:
            self._binary = bin(self.hash)[2:].zfill(27)

        return self._binary

    @binary.setter
    def binary(self,value):
        pass

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self,value):
        pass

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self,value):
        pass

class Cell4(Cell):

    _Refs   = weakref.WeakValueDictionary()
    _Hashes = weakref.WeakValueDictionary()

    MODE   = TTT_4_IN_A_ROW

    def __new__(cls,number,player=FREE_SPACE):

        return create_and_verify_cell(number=number,
                                      player=player,
                                      cell_class=cls)

class Cell5(Cell):

    _Refs   = weakref.WeakValueDictionary()
    _Hashes = weakref.WeakValueDictionary()

    MODE   = TTT_5_IN_A_ROW

    def __new__(cls,number,player=FREE_SPACE):

        return create_and_verify_cell(number=number,
                                      player=player,
                                      cell_class=cls)



