
FREE_SPACE = 0
PLAYER_1   = 1
PLAYER_2   = 2

MARKS = {
    FREE_SPACE : '[]',
    PLAYER_1   : 'X',
    PLAYER_2   : 'O'
}

PLAYERS    = {
    FREE_SPACE : 'EMPTY CELL',
    PLAYER_1   : 'Player 1',
    PLAYER_2   : 'Player 2'
}


GRID         = 0
GRID_STATE   = 1
LINE         = 2
GRID_4       = 3
GRID_STATE_4 = 4
LINE_4       = 5
GRID_5       = 6
GRID_STATE_5 = 7
LINE_5       = 8


MODES = {
        GRID:{
            'mode'   : 'Grid',
            'length' : 27
        },
        GRID_4:{
            'mode'   : 'Grid 4',
            'length' : 48
        },
        GRID_5:{
            'mode'   : 'Grid 5',
            'length' : 75
        },
        GRID_STATE:{
            'mode'   : 'Grid State',
            'length' : 9
        },
        GRID_STATE_4:{
            'mode'   : 'Grid State 4',
            'length' : 16
        },
        GRID_STATE_5:{
            'mode'   : 'Grid State 5',
            'length' : 25
        },
        LINE:{
            'mode'   : 'Line',
            'length' : 3
        },
        LINE_4:{
            'mode'   : 'Line 4',
            'length' : 4
        },
        LINE_5:{
            'mode'   : 'Line 5',
            'length' : 5
        }}


TTT_3_IN_A_ROW  =  0
TTT_4_IN_A_ROW  =  1
TTT_5_IN_A_ROW  =  2

GAME_MODES = {
    TTT_3_IN_A_ROW:{
        'GRID'       : GRID ,
        'GRID_STATE' : GRID_STATE ,
        'LINE'       : LINE,
    },
    TTT_4_IN_A_ROW:{
        'GRID'       : GRID_4,
        'GRID_STATE' : GRID_STATE_4,
        'LINE'       : LINE_4,
    },
    TTT_5_IN_A_ROW:{
        'GRID'       : GRID_5,
        'GRID_STATE' : GRID_STATE_5,
        'LINE'       : LINE_5
    }
}


def available_modes():

    mode_text  = "{} with a mode value of {} with a bit size length of {}"
    modes = [mode_text.format(MODES[m]['mode'],m,MODES[m]['length']) for m in MODES]
    return " ,or ".join(modes)

