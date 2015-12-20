
from tictactoe.errors    import InvalidHash, InvalidCell
from tictactoe.hash.hash import Hashable
from tictactoe.settings  import FREE_SPACE
from tictactoe.utils     import verify_player, verify_cell, verify_binary, compute_hash


class Cell(Hashable):

    def __init__(self,number,player=FREE_SPACE):

        verify_player(player=player)
        verify_cell(cell=number)

        self._number = number
        self._player = player

        self._hash = None
        self._binary = None

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

        verify_binary(binary=binary)

        if isinstance(binary,(list,tuple)):
            binary = "".join([str(n) for n in binary])


        binary = "".join([b for b in reversed(binary)])

        cls.validate_binary(binary=binary)
        cell, player = cls.decompose_binary(index=binary.index('1'))

        return cls(number=cell,player=player)

    @classmethod
    def from_hash(cls,hash):
        if not isinstance(hash,int):
            raise InvalidHash('A {} type was passed to hash. Only '
                              'an int type is acceptable'.format(type(hash)))

        binary = "".join([b for b in reversed(bin(hash)[2:].zfill(27))])

        cls.validate_binary(binary=binary)
        cell, player = cls.decompose_binary(index=binary.index('1'))

        return cls(number=cell,player=player)

    @property
    def hash(self):
        if self._hash is None:
            self._hash = compute_hash(cell=self.number,
                                      player=self.player)

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


