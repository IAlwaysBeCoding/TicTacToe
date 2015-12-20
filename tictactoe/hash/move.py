
from tictactoe.hash.cell import Cell
from tictactoe.utils     import verify_real_player

class Move(Cell):

    def __init__(self,cell,player):
        verify_real_player(player=player)
        super(Move,self).__init__(number=cell,player=player)


