

from itertools import  combinations_with_replacement

from rome import Roman

from tictactoe.compute      import player_combinations
from tictactoe.settings     import (FREE_SPACE, PLAYER_1, PLAYER_2, PLAYERS ,
                                   TTT_3_IN_A_ROW, MODES, GAME_MODES, MARKS)
from tictactoe.verification import verify_player, verify_real_player, verify_game_mode



PLAYER_MAP = {
    FREE_SPACE : 'player_0',
    PLAYER_1   : 'player_1',
    PLAYER_2   : 'player_2'
}



def generate_player_keys():
    return dict([(PLAYER_MAP[key],0) for key in PLAYER_MAP])


def generate_combinations(players_to_combine,length):


    if not isinstance(players_to_combine,(list,tuple)):
        raise TypeError(
                'players_to_combine  needs to be a list with 1 or 2 '\
                'items : {} as player_0 , {} as player_1 and ' \
                '{} as player_2 .No other items besides '\
                'those .'.format(FREE_SPACE,PLAYER_1,PLAYER_2))

    for p in players_to_combine:
        verify_player(player=p)


    combinations = []

    for pattern in combinations_with_replacement(players_to_combine,length):
        pattern_combinations = player_combinations(
                                             player_0 = pattern.count(FREE_SPACE),
                                             player_1 = pattern.count(PLAYER_1) ,
                                             player_2 = pattern.count(PLAYER_2)
                                             )

        for combination in pattern_combinations:
            p = [combination.count(FREE_SPACE),
                 combination.count(PLAYER_1) ,
                 combination.count(PLAYER_2)]

            if p not in combinations:
                combinations.append(p)

    return combinations


