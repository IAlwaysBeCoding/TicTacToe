"""
The Cell is what every Tic Tac Toe Game is made of.
===

A `Cell` is a basic piece of the Tic Tac Toe game that represents an empty cell or
a player's marked(either **Player 1** or **Player 2**), regardless of what
dimension or **n-in-a-row** the game is played on. It is also a `Hashable` instance
that means it can be constructed from a *hash* as well.Now, a `Cell` is simply a `Hashable`
object that provides 2 additional class *method* **properties**:

* `number` : This property returns the `Cell` index. That is, the
            `Cell`'s number. For example, in a regular **3-in-a-row** Tic Tac Toe
            game(2D). There are 9 total cells(3x3),and the only valid `Cell`
            numbers are **_1-9_**. In a **4-in-a-row** Tic Tac Toe game(2d)
            the total number of cells are **_1-16_**.

* `player` : A `Cell` can only represent an _empty space_(*FREE_SPACE*) or either
            **Player 1** or **Player 2**. Therefore, the only possible values are
            `FREE_SPACE`(0), `PLAYER_1`(1), AND `PLAYER_2`(2).

Here is an example

    #!python
    #Let x = Player 1's mark
    #Let o = Player 2's mark
    #Let - = an empty cell or **Player 0** mark
    #|-|x|-|
    #|-|-|-|
    #|-|-|-|
    #Represents a Player 1's mark on cell 2.
    mark = Cell(number=2,player=1)
    print(mark.hash) # This equals 16

"""
import weakref

from tictactoe.compute      import compute_hash
from tictactoe.errors       import TicTacToeException
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

    """
         `Cell` provides all of `Hashable` methods plus 2 more
         other class *property* methods:

         * `number` : Represents the `Cell` unique number.
         * `player` : This is either a representation of an emtpy cell
                    or a **Player 1**'s or **Player 2**'s marking.
    """

    _Refs   = weakref.WeakValueDictionary()
    _Hashes = weakref.WeakValueDictionary()

    MODE   = TTT_3_IN_A_ROW

    def __new__(cls,number,player=FREE_SPACE):
        """
            Implementing a **__new__** method instead of the most *ubiquitious*
            method **__init__** allows us to keep saving memory by not having the
            same `Cell` instances created more than once. That is, everytime you construct
            a new `Cell` instance when a previous `Cell` was constructed early on with the
            same `hash` value(same `number` and `player` property), then it
            returns the previously one created that is stored inside a **_Refs**
            or **_Hashes**. If you check the id of both `Cell` instances through the
            id() method , then you will see that they are exactly the same object.
        """

        return create_and_verify_cell(number=number,
                                      player=player,
                                      cell_class=cls)
    @staticmethod
    def decompose_binary(index):
        return ((index / 3) + 1, index % 3)

    @staticmethod
    def validate_binary(binary):
        if binary.count('1') != 1:
            raise TicTacToeException(
                'Binary:{} is an invalid Cell. Only a single '\
                '1 can be found in the binary'.format(binary))

    @classmethod
    def from_binary(cls,binary):
        """
            This returns a new `Cell` instance by using a binary representation
            either through a *string* representing the a cell in 0's and 1's, or
            using a list/tuple with only valid items being again 0's and 1's.

            The binary representation will be the size of the `Grid`.In other words
            if you wanted to represent **Player 1**'s mark on cell number 2
            in a 3x3(2d) Tic Tac Toe game, then you will need a str or list/tuple
            like this :

                 binary = '000000000000000000000010000'
                 binary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
                 binary = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','1','0','0','0','0']

                 cell = Cell.from_binary(binary)

        """

        verify_binary(binary=binary,mode=GAME_MODES[cls.MODE]['GRID'])
        if isinstance(binary,(list,tuple)):
            binary = "".join([str(n) for n in binary])


        binary = "".join([b for b in reversed(binary)])

        cls.validate_binary(binary=binary)
        cell, player = cls.decompose_binary(index=binary.index('1'))

        return cls(number=cell,player=player)

    @classmethod
    def from_hash(cls,hash):
        """
            This is the alternative method to construct a new `Cell` from a **hash** value.
            It only takes a valid hash of a `Cell` , anything else and it will raise a
            **TicTacToeException** or **TicTacToeHashException**.
        """
        if not isinstance(hash,(long,int)):
            raise TicTacToeException('A {} type was passed to hash. Only '
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
        """
            Returns the an `int` or a `long` representing hash
            of the current `Cell` instance. This is the same
            value that will be returned when the object is *hashed*
            through the python native **hash()** method.
        """
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

        """
            Returns the binary representation of the current `Cell` instance. However,
            it is important to notice that the binary representation is in **Big Endian**
            mode.
        """
        if self._binary is None:
            self._binary = bin(self.hash)[2:].zfill(27)

        return self._binary

    @binary.setter
    def binary(self,value):
        pass

    @property
    def number(self):
        """
            This property represents the current `Cell` number of the Tic Tac Toe game.
            So, a 3x3 Tic Tac Toe game in a 2d game will have at most 9 cells, and the
            possible `Cell` numbers allowed are anything between **1-9**.

        """
        return self._number

    @number.setter
    def number(self,value):
        pass

    @property
    def player(self):
        """
            Player's number.This can be either **FREE_SPACE**(0) for basically free space,
            **PLAYER_1**(1) or **PLAYER_2**(2).
        """
        return self._player

    @player.setter
    def player(self,value):
        pass

class Cell4(Cell):

    """
        This is a `Cell` subclass that provides everything inside `Cell`
        but extends the cell number from **1-9**  to **1-16**, to provide
        the right numbering for 4-IN-A-ROW game.
    """

    _Refs   = weakref.WeakValueDictionary()
    _Hashes = weakref.WeakValueDictionary()

    MODE   = TTT_4_IN_A_ROW

    def __new__(cls,number,player=FREE_SPACE):

        return create_and_verify_cell(number=number,
                                      player=player,
                                      cell_class=cls)

class Cell5(Cell):

    """
        This is a `Cell` subclass that provides everything inside `Cell`
        but extends the cell number from **1-9**  to **1-25**, to provide
        the right numbering for 5-IN-A-ROW game.
    """

    _Refs   = weakref.WeakValueDictionary()
    _Hashes = weakref.WeakValueDictionary()

    MODE   = TTT_5_IN_A_ROW

    def __new__(cls,number,player=FREE_SPACE):

        return create_and_verify_cell(number=number,
                                      player=player,
                                      cell_class=cls)



