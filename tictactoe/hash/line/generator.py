

from rome import Roman

from tictactoe.compute         import player_combinations
from tictactoe.errors          import TicTacToeException
from tictactoe.hash.line       import PLAYER_MAP, generate_player_keys, generate_combinations
from tictactoe.hash.line.state import LineState
from tictactoe.settings        import (FREE_SPACE, PLAYER_1, PLAYER_2, PLAYERS ,
                                      TTT_3_IN_A_ROW, MODES, GAME_MODES, MARKS)
from tictactoe.verification    import verify_player, verify_real_player, verify_game_mode



class LineStateGenerator(object):

    def __init__(self,game_mode=TTT_3_IN_A_ROW):

        verify_game_mode(game_mode=game_mode)
        self._mode = GAME_MODES[game_mode]['LINE']
        self._length  = MODES[self.mode]['length']

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self,value):
        pass

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self):
        pass

    def create_line_state_name(self,player_0,player_1,player_2):

        for player in [player_0, player_1, player_2]:
            if isinstance(player,str) and player.isdigit():
                continue

            if not isinstance(player,int):
                raise TicTacToeException(
                    'Invalid type:{} for {}.An int must be passed'.format(type(player),
                                                                          PLAYERS[player]))

        length = sum([int(player_0), int(player_1) ,int(player_2)])
        if length != self._length:
            raise TicTacToeException(
                'Current line length: {}. Line length must be :{}'.format(length,self._length))

        return '{}:{}/{}:{}/{}:{}'.format(MARKS[FREE_SPACE],
                                     Roman(player_0) if int(player_0) != 0 else '',
                                     MARKS[PLAYER_1],
                                     Roman(player_1) if int(player_1) != 0 else '',
                                     MARKS[PLAYER_2],
                                     Roman(player_2) if int(player_2) != 0 else '')

    def create_line_state(self,player_0,player_1,player_2):

        state_name   = self.create_line_state_name(player_0,player_1,player_2)
        combinations = player_combinations(player_0,player_1,player_2)

        return LineState(name=state_name,permutations=combinations,length=self.length)

    def full_line_state(self,player):

        verify_player(player=player)
        players = generate_player_keys()
        players[PLAYER_MAP[player]] = self.length

        return self.create_line_state(**players)

    def non_blocked_states(self,player):
        verify_real_player(player=player)

        lines = []
        for i in xrange(1,self.length,1):

            players = generate_player_keys()
            del players[ PLAYER_MAP[FREE_SPACE] ]
            players[ PLAYER_MAP[player] ] = i

            line = self.create_line_state(self.length-i,**players)
            lines.append(line)

        return lines

    def blocked_states(self,player):
        verify_real_player(player=player)

        lines = []
        opponent = PLAYER_1 if player == PLAYER_1 else PLAYER_2

        for i in xrange(1,self.length,1):

            players = generate_player_keys()
            fill_players = dict(PLAYER_MAP)
            del players[ PLAYER_MAP[player] ]
            del fill_players[ player ]

            for raw_combination in generate_combinations(fill_players.keys(),self.length-i):
                raw_combination[opponent] + 1
                raw_combination[player]  = i

                if (raw_combination[FREE_SPACE] + raw_combination[player] != self.length):
                    lines.append(self.create_line_state(*raw_combination))

        return lines

