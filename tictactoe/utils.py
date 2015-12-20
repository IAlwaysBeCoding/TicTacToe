
from functools import partial
from itertools import ifilterfalse

from tictactoe.errors import (InvalidBinary, InvalidGrid, InvalidPlayer,
                              InvalidCellNumber, InvalidBinaryMode,
                              InvalidHash, InvalidHashMode)
from tictactoe.settings import (FREE_SPACE, PLAYER_1, PLAYER_2, GRID, GRID_STATE,
                                MODES)


def available_modes():

    mode_text  = "{} with a mode value of {} with a bit size length of {}"
    modes = [mode_text.format(MODES[m]['mode'],m,MODES[m]['length']) for m in MODES]
    return " ,or ".join(modes)


def verify_player(player):
    if player not in (FREE_SPACE, PLAYER_1, PLAYER_2):
        raise InvalidPlayer(
            'Invalid value for player.Only acceptable ' \
            'values are {} for Player 1, {} for Player 2 '\
            ' or {} for an Empty Cell'.format(PLAYER_1,PLAYER_2,FREE_SPACE))


def verify_real_player(player):
    if player not in (PLAYER_1, PLAYER_2):
        raise InvalidPlayer('Invalid real player. Only real ' \
                            'players are acceptable.Player 1 ' \
                            ':{} or Player 2:{}'.format(PLAYER_1,PLAYER_2))


def verify_cell(cell):
    if cell < 1 or cell > 9:
        raise InvalidCellNumber('Cell needs to a number between 1-9')


def verify_grid(grid):

    if not isinstance(grid,(list,tuple)):
        raise InvalidGrid('Grid needs to be a list')

    if len(grid) != 9:
        raise InvalidGrid('Grid needs to be a list of length 9 '\
                          'containing only possible values '\
                          '{} for Free Space, {} for Player1 or '\
                          '{} for Player2'.format(FREE_SPACE, PLAYER_1, PLAYER_2))

    for n in grid:
        try:
            int(n)
        except ValueError:
            raise InvalidGrid(
                'Found an invalid character:{}. Characters that ' \
                'are not Free Space:{} Player1:{} , Player2:{} ' \
                'are invalid.'.format(n, FREE_SPACE, PLAYER_1, PLAYER_2))

    iterate_non_player = partial(ifilterfalse,
                        lambda n : (int(n) == FREE_SPACE) or \
                                   (int(n) == PLAYER_1)   or \
                                   (int(n) == PLAYER_2))

    grid_array = [int(n) for n in grid]

    for non_players in iterate_non_player(grid_array):
        raise InvalidGrid(
            'Found an invalid character:{}. Characters that ' \
            'are not Free Space({}) value, or Player1({}) value, '\
            'or Player2({}) value are invalid.'.format(non_players, FREE_SPACE, PLAYER_1, PLAYER_2))


def verify_hash(hash,mode=GRID):

    if not isinstance(hash,int):
        raise InvalidHash('Hash must be an int')

    for m in [GRID,GRID_STATE]:
        if m == mode:
            if hash < 0 or hash >= (1 << MODES[mode]['length']):
                InvalidHash(
                    'An invalid hash:{} was passed for mode:{}, '\
                    'only hash acceptables are from 0-{}'.format(hash,
                                                                mode,
                                                                (1 << MODES[mode]['length'] -1)))
            else:
                break
    else:
        raise InvalidHashMode(
            'An invalid hash mode was found:{} '\
            'only acceptable modes are :{} '.format(mode, available_modes()))


def verify_binary(binary,mode=GRID):

    for m in [GRID,GRID_STATE]:
        if m == mode:
            check_length = MODES[mode]['length']
            break
    else:
       raise InvalidBinaryMode(
            'An invalid binary mode was found:{} '\
            'only acceptable binary modes are :{} '.format(mode, available_modes()))

    if isinstance(binary,(list,tuple,str)):

        if len(binary) != check_length:
            raise InvalidBinary(
                'Found a {} with {} items.The binary '\
                'representation needs to be a {} bit ' \
                'binary representation'.format(type(binary), len(binary), check_length))


        if isinstance(binary,(list,tuple)):
            for n in binary:
                try:
                    int(n)
                except ValueError:
                    raise InvalidBinary(
                        'Found an invalid character:{}. Characters that ' \
                        'are not 0 or 1 are invalid.'.format(n))

        else:
            if not binary.isdigit():
                raise InvalidBinary(
                    'Binary does not include all digits.Non-number '\
                    ' characters were found')

        iterate_non_binary = partial(ifilterfalse,lambda n : (int(n) == 0) or (int(n) == 1))
        bin_array = [int(n) for n in binary]

        for non_bin in iterate_non_binary(bin_array):
            raise InvalidBinary(
                'Found an invalid character:{}. Characters that ' \
                'are not 0 or 1 are invalid.'.format(non_bin))


    else:
        raise InvalidBinary('Binary is not a str, list, or tuple containing 0 and 1. '\
                            'Instead, a {} type was found'.format(type(binary)))


def decompose_grid_hash(hash):

    verify_hash(hash=hash)
    binary = bin(hash)[2:].zfill(27)
    binary_cells = [c for c in
                        reversed(
                                    [binary[bin_range:bin_range+3]
                                    for bin_range in xrange(0, len(binary), 3)]
                                )
                    ]

    bits_to_push = lambda c : ((c+1) * 3) - 3

    return [ (1 << ((int(b, 2) >> 1) + bits_to_push(c=cell)))
            for cell, b in enumerate(binary_cells) ]


def compute_hash(cell,player):

    verify_player(player=player)
    verify_cell(cell=cell)

    bits_to_push = (cell * 3) - 3

    return (1 << player + bits_to_push)

def compute_all_hash_moves(player):
    return [compute_hash(cell=c,player=player) for c in xrange(1, 10, 1)]


def get_all_possible_lines():

    horizontal = [tuple(y for y in xrange(x, 10, 3)) for x in xrange(1, 4)]
    vertical   = [tuple(y for y in xrange(x, x+3, 1)) for x in xrange(1, 10, 3)]
    diagnol    = [tuple(xrange(3, 8, 2)) , tuple(xrange(1, 10, 4))]

    return horizontal + vertical + diagnol


def new_game_hash(sum_cells=False):

    grid = [compute_hash(cell=c,player=FREE_SPACE) for c in xrange(1, 10, 1)]
    return sum(grid) if sum_cells else grid


