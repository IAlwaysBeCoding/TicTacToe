
from itertools import ifilterfalse

from tictactoe.errors         import TicTacToeLineException
from tictactoe.hash.grid      import Grid, Grid4, Grid5
from tictactoe.line.generator import LineStateGenerator
from tictactoe.settings       import (GAME_MODES, MODES, TTT_3_IN_A_ROW, TTT_4_IN_A_ROW,
                                      TTT_5_IN_A_ROW)


class Line(object):

    MODE_KEY = lambda game_mode : MODES[GAME_MODES[game_mode]['LINE']]['length']

    GENERATORS = {
        TTT_3_IN_A_ROW : LineStateGenerator(game_mode=TTT_3_IN_A_ROW),
        TTT_4_IN_A_ROW : LineStateGenerator(game_mode=TTT_4_IN_A_ROW),
        TTT_5_IN_A_ROW : LineStateGenerator(game_mode=TTT_5_IN_A_ROW)
    }

    STATES = {
        TTT_3_IN_A_ROW : GENERATORS[TTT_3_IN_A_ROW].all_states(),
        TTT_4_IN_A_ROW : GENERATORS[TTT_4_IN_A_ROW].all_states(),
        TTT_5_IN_A_ROW : GENERATORS[TTT_5_IN_A_ROW].all_states()
    }

    GRIDS  = {
        Grid   : MODE_KEY(game_mode=TTT_3_IN_A_ROW),
        Grid4  : MODE_KEY(game_mode=TTT_4_IN_A_ROW),
        Grid5  : MODE_KEY(game_mode=TTT_5_IN_A_ROW)
    }


    def __init__(self,grid,indexes):

        if type(grid) not in self.GRIDS:
            raise TicTacToeLineException(
                'Invalid grid. Grid needs to be an instance of :{}'.format(self.GRIDS.keys()))

        self._grid = grid
        self._indexes = indexes
        self.verify_indexes()

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self,value):
        pass

    def length(self):
        return self.GRIDS[type(self.grid)]

    def indexes(self):
        return self._indexes

    def verify_indexes(self):
        length = self.length()

        if length != len(self.indexes()):
            raise TicTacToeLineException(
                'Indexes contain incorrect number of indexes. Grid {} type requires ' \
                '{} total indexes.'.format(type(self.grid),length))

        min_value = 0
        max_value = (length * length ) - 1
        not_valid_index = lambda i : i >= 0 and  i <=  max_value

        for maybe_invalid in ifilterfalse(not_valid_index,self.indexes()):
            raise TicTacToeLineException(
                'Found an invalid index :{}. Only valid indexes from :{} to {} ' \
                'are valid for Grid :{}'.format(maybe_invalid,min_value,max_value,type(self.grid)))


    def hash(self):
        return sum([self.grid[i+1].hash for i in self.indexes()])

