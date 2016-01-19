"""
Grid is the the main representation of a Tic Tac Toe game containing all the cells of the game.
===


"""


from itertools import chain

from tictactoe.compute            import (compute_hash, compute_all_hash_moves, new_game_hash,
                                          decompose_grid_hash)
from tictactoe.errors             import (TicTacToeException, TicTacToeHashException, IncompatibleGrid,
                                          CellIsTaken)
from tictactoe.hash               import Hashable
from tictactoe.hash.cell          import Cell, Cell4, Cell5
from tictactoe.hash.move          import Move, Move4, Move5
from tictactoe.hash.state         import GridState, GridState4, GridState5
from tictactoe.hash.transposition import HashTable
from tictactoe.settings           import (FREE_SPACE, PLAYER_1, PLAYER_2, GAME_MODES,
                                         TTT_3_IN_A_ROW, TTT_4_IN_A_ROW, TTT_5_IN_A_ROW)
from tictactoe.verification       import (verify_cell, verify_player, verify_grid, verify_binary,
                                          verify_hash, verify_game_mode)



def create_player_hash_table(mode=TTT_3_IN_A_ROW):
    verify_game_mode(game_mode=mode)

    cell_klass = {
        TTT_3_IN_A_ROW : Cell,
        TTT_4_IN_A_ROW : Cell4,
        TTT_5_IN_A_ROW : Cell5
    }

    players = (FREE_SPACE, PLAYER_1, PLAYER_2)
    player_hashes = lambda players,m : [compute_all_hash_moves(player=p,mode=m) for p in players]

    hashes = list(chain.from_iterable(player_hashes(players,mode)))

    player_hash_table = dict([(h,cell_klass[mode].from_hash(hash=h)) for h in hashes])

    return HashTable(table=player_hash_table)


CELL_HASH_TABLE = {
    TTT_3_IN_A_ROW : create_player_hash_table(mode=TTT_3_IN_A_ROW),
    TTT_4_IN_A_ROW : create_player_hash_table(mode=TTT_4_IN_A_ROW),
    TTT_5_IN_A_ROW : create_player_hash_table(mode=TTT_5_IN_A_ROW)
}


class Grid(Hashable):

    MODE = TTT_3_IN_A_ROW

    GRID_STATE_KLASS = GridState

    CELL_KLASS = Cell

    MOVE_KLASS = Move

    def __init__(self,hash=None):
        if hash is None:
            hash = new_game_hash(sum_cells=True,mode=self.MODE)

        verify_hash(hash=hash,mode=GAME_MODES[self.MODE]['GRID'])
        self._hash  = hash
        self._binary = None
        self._hash_map = CELL_HASH_TABLE[self.MODE]
        self._cells = [self.CELL_KLASS.from_hash(hash=h)
                       for h in decompose_grid_hash(hash=self._hash,mode=self.MODE)]

        state_hash = sum([ ( 1 << n) for n, c in enumerate(self._cells)
                        if (c.player == PLAYER_1 or c.player == PLAYER_2)])

        self._state = self.GRID_STATE_KLASS(hash=state_hash)
        self.validate_grid()

    def __getitem__(self,cell):
        return self.get_cell(number=cell)

    def __setitem__(self,key,value):

        """ The only proper way to change a grid is to apply a new
            grid or to apply a move to the current grid. Please do not
            touch any of the internal properties. We all know python is
            an adult consenting language and there are no private variables
            anywhere.However, if you change any Cell or even the GridState, then
            the great gods of programming will strike you while you sleep.
            You have been warned!
        """
        pass

    def __call__(self,hash):
        return self.look_up_hash(hash=hash)

    @classmethod
    def from_binary(cls,binary):
        verify_binary(binary,mode=GAME_MODES[cls.MODE]['GRID'])
        return cls(hash=int(binary, 2))

    @classmethod
    def from_array(cls,array):
        verify_grid(array,mode=cls.MODE)
        grid_hash = sum([compute_hash(cell=c+1,player=p,mode=cls.MODE) for c,p in enumerate(array)])

        return cls(hash=grid_hash)

    @property
    def hash(self):
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

    def cells_taken(self,player=FREE_SPACE):

        verify_player(player=player)

        if player != FREE_SPACE:
            return [self[n] for n in self._state.get_taken_cells()
                    if self[n].player == player]

        else:
            return [self[n] for n in self._state.get_free_cells()]

    def total_free_cells(self):
        return self._state.free

    def total_taken_cells(self):
        return self._state.taken

    def get_cell(self,number):

        verify_cell(cell=number,mode=self.MODE)
        return self._cells[number-1]

    def look_up_hash(self,hash):

        try:
            player, cell = self._hash_map[hash]

        except KeyError:
            raise TicTacToeException(
                'An invalid hash:{} that contained no valid' \
                'cell number and player was passed to Grid.'.format(hash))

        else:
            return self.CELL_KLASS(number=cell, player=player)

    def validate_grid(self):
        total_taken = self.total_taken_cells()

        if total_taken != 0:
            player_1_cells = len(self.cells_taken(player = PLAYER_1))
            player_2_cells = len(self.cells_taken(player = PLAYER_2))

            if (player_1_cells != player_2_cells) and (player_1_cells - 1 != player_2_cells):
                raise TicTacToeHashException(
                    'Invalid grid setup, Player1 has {} moves while ' \
                    'Player2 has {} moves.Grid is not a valid '\
                    'Tic Tac Toe grid'.format(player_1_cells,player_2_cells))

    def apply_grid(self,grid,backwards=False):

        if not isinstance(grid,Grid):
            raise TicTacToeHashException(
                'grid is not a valid Grid instance. Instead a {}' \
                'instance was passed.Cannot apply Grid'.format(type(grid)))

        applied_hash = self.hash | grid.hash
        applied_grid = [Cell.from_hash(hash=h) for h in decompose_grid_hash(hash=applied_hash,mode=self.MODE)]

        for c in applied_grid:

            if (self[c.number].player != FREE_SPACE) and (c.player != self[c.number].player):

                raise CellIsTaken(
                    'Cell {} has been taken by player {} already, ' \
                    'and cannot override Grid.Grid applied ' \
                    'failed'.format(c.number,self[c.number].player))

        if not backwards:
            if applied_hash != grid.hash:
                raise IncompatibleGrid(
                    'New grid cannot go backwards in moves. Must provide all the '\
                    'previous moves plus 1 or more moves.')

        return self if applied_hash == self.hash else self.GRID_KLASS(hash=applied_hash)

    def apply_move(self,move):

        if not isinstance(move,self.MOVE_KLASS):
            raise TicTacToeHashException(
                'move is not a valid Move instance. Instead a {}' \
                'instance was passed.Cannot apply Move'.format(type(move)))

        if (self[move.number].player != FREE_SPACE) and (move.player != self[move.number].player):
            raise CellIsTaken(
                'Cell {} has been taken by player {} already, ' \
                'and cannot override Move.Move applied ' \
                'failed'.format(move.number,self[move.number].player))

        elif self[move.number].player == move.player:
            return self

        else:

            cells = [c for c in self._cells]
            cells[move.number-1] = move

            return type(self)(hash=sum([c.hash for c in cells]))

class Grid4(Grid):

    MODE = TTT_4_IN_A_ROW

    GRID_STATE_KLASS = GridState4

    CELL_KLASS = Cell4

    MOVE_KLASS = Move4

class Grid5(Grid):

    MODE = TTT_5_IN_A_ROW

    GRID_STATE_KLASS = GridState5

    CELL_KLASS = Cell5

    MOVE_KLASS = Move5

