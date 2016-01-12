
from tictactoe.errors       import TicTacToeException
from tictactoe.settings     import FREE_SPACE, PLAYER_1, PLAYER_2, MODES, LINE
from tictactoe.verification import verify_player


class LineState(object):

    def __init__(self,name,permutations,length=MODES[LINE]['length']):

        self._name = name

        self._length = length
        self._permutations = permutations
        self.validate_permutations()

        self._player_0 = None
        self._player_1 = None
        self._player_2 = None

    def __repr__(self):

        return 'LineState(name="{}",length={})'.format(self.name,self.length)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,value):
        pass

    @property
    def permutations(self):
        return self._permutations

    @permutations.setter
    def permutations(self,value):
        pass

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self,value):
        pass

    @property
    def player_0(self):
        if self._player_0 is None:
            self._player_0 = self.player(player=FREE_SPACE)

        return self._player_0

    @player_0.setter
    def player_0(self,value):
        pass

    @property
    def player_1(self):
        if self._player_1 is None:
            self._player_1 = self.player(player=PLAYER_1)

        return self._player_1

    @player_1.setter
    def player_1(self,value):
        pass

    @property
    def player_2(self):
        if self._player_2 is None:
            self._player_2 = self.player(player=PLAYER_2)

        return self._player_2

    @player_2.setter
    def player_2(self,value):
        pass

    def player(self,player):
        verify_player(player=player)
        return  self._permutations[0].count(player)

    def validate_permutations(self):

        if not isinstance(self.permutations,(list,tuple)):
            raise TicTacToeException(
                'Invalid permutation type:{} . A list or tuple must ' \
                'be passed containing the different line permutations ' \
                'with only possible values {} for Free Space, {} for ' \
                'Player 1, and {} for Player 2'.format(type(self.permutations),
                                                       FREE_SPACE,
                                                       PLAYER_1,
                                                       PLAYER_2))

        if len(self.permutations) == 0:
            raise TicTacToeException(
                'permutations is an empty list/tuple. It contains no permutations')

        invalids = filter(lambda p : len(p) != self.length, self.permutations)

        if invalids:
            raise TicTacToeException(
                'Found invalid permutation(s):{} .Line length must be atleast:{} '\
                'for each permutation'.format(invalids,self.length))

