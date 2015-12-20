
from funcy import  memoize

from tictactoe.hash.hash import Hashable
from tictactoe.settings  import GRID_STATE
from tictactoe.utils     import verify_binary, verify_hash


class GridState(Hashable):

    def __init__(self,hash=0):

        verify_hash(hash=hash,mode=GRID_STATE)
        self._hash = hash
        self._binary = None

    @classmethod
    def from_binary(cls,binary):

        verify_binary(binary,mode=GRID_STATE)
        return cls(hash=int(binary, 2))

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self,value):
        pass

    @property
    def binary(self):
        if self._binary is None:
            self._binary = bin(self.hash)[2:].zfill(9)

        return self._binary

    @binary.setter
    def binary(self,value):
        pass

    @property
    def free(self):
        return self.binary.count('0')

    @property
    def taken(self):
        return self.binary.count('1')

    @memoize
    def get_taken_cells(self):
       return [i+1 for i,b in enumerate(reversed(self.binary)) if b == '1']

    @memoize
    def get_free_cells(self):
       return [i+1 for i,b in enumerate(reversed(self.binary)) if b == '0']



