

from itertools import  permutations, chain

from tictactoe.errors       import TicTacToeException
from tictactoe.settings     import (FREE_SPACE, PLAYER_1, PLAYER_2, PLAYERS,
                                    TTT_3_IN_A_ROW, MODES, GAME_MODES)
from tictactoe.verification import (verify_player, verify_hash, verify_game_mode,
                                    verify_cell)



def player_combinations(player_0,player_1,player_2):

    for player in [player_0,player_1,player_2]:

        if isinstance(player,str) and player.isdigit():
            continue

        if not isinstance(player,int):
            raise TicTacToeException(
                'Invalid type:{} for {}.An int must be passed'.format(type(player),PLAYERS[player]))


    players = chain.from_iterable([
                [p[1] for c in xrange(0,int(p[0]),1)]
                for p in ((player_0, FREE_SPACE),
                          (player_1, PLAYER_1),
                          (player_2, PLAYER_2))
                ])
    return list(set(permutations(players)))

def decompose_grid_hash(hash,mode=TTT_3_IN_A_ROW):

    verify_game_mode(game_mode=mode)
    m = GAME_MODES[mode]['GRID']
    verify_hash(hash=hash,mode=GAME_MODES[mode]['GRID'])
    length = MODES[m]['length']
    binary = bin(hash)[2:].zfill(length)
    binary_cells = [c for c in
                        reversed(
                                    [binary[bin_range:bin_range+3]
                                    for bin_range in xrange(0, len(binary), 3)]
                                )
                    ]

    bits_to_push = lambda c : ((c+1) * 3) - 3

    return [ (1 << ((int(b, 2) >> 1) + bits_to_push(c=cell)))
            for cell, b in enumerate(binary_cells) ]

def compute_hash(cell,player,mode=TTT_3_IN_A_ROW):

    verify_player(player=player)
    verify_cell(cell=cell,mode=mode)

    bits_to_push = (cell * 3) - 3

    return (1 << player + bits_to_push)

def compute_all_hash_moves(player,mode=TTT_3_IN_A_ROW):
    verify_game_mode(game_mode=mode)
    key = lambda m : GAME_MODES[m]['GRID_STATE']
    length = MODES[key(m=mode)]['length'] + 1
    return [compute_hash(cell=c, player=player,mode=mode) for c in xrange(1, length, 1)]

def get_all_possible_lines():

    horizontal = [tuple(y for y in xrange(x, 10, 3)) for x in xrange(1, 4)]
    vertical   = [tuple(y for y in xrange(x, x+3, 1)) for x in xrange(1, 10, 3)]
    diagnol    = [tuple(xrange(3, 8, 2)) , tuple(xrange(1, 10, 4))]

    return horizontal + vertical + diagnol

def new_game_hash(sum_cells=False,mode=TTT_3_IN_A_ROW):

    grid = compute_all_hash_moves(player=FREE_SPACE,mode=mode)
    return sum(grid) if sum_cells else grid


