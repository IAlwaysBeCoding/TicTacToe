"""
Making hashes from hashable objects
===

To make a **_tic-tac-toe_** game it was necessary to create every **move**, **cell**, **board**, **game position**
as a `hash`. In a sense, it would be very useful to be able to _reproduce_ these _basic_ **things** :

* `Cell` : A place where a player could place a mark.
* `Move`: Player 1's or Player 2's move
* `Grid` : An array containing all the cells in the board.

Plus, you _could_ also represent different kind of `states` using **hashable** objects, such
*hypothetical* **states** could be:

* `GridState` : This can be a set of bits representing what cells are **taken**
(by __Player 1__ or __Player 2__) or __free__(_unmarked_!). They can be **useful** to **AI**
components for avoiding _useless_ computation from having to get the state of each `cell`.

![Board States](../../assets/f10_16.gif)


A super basic _abstract_ `meta class` would be the way to go for all **hashable** objects to inherit from.
So, a `Hashable` object provides 5 basic features :

1. Construction method from a **hash** into a new `Hashable` instance by either
one of this methods:
    * `from_hash` : This would be an alternative construction method that takes a
        hash and returns a new `Hashable` instance if success.
    * `__init__` : You could also start a new `Hashable` instance through the
        regular construction mechanism.

2. Another construction method to create a `Hashable` object but this time from a  **binary**(_0's_ and/or _1's_) representation.
3. Two properties:
    * `hash` : an integer representing the *hash*.
    * `binary` : a representation of the property `hash` as _0's_ and _1's_.
4. 2 important magic methods :
    * ** \_\_eq\_\_ **:  An essential method for comparing the current instance
    * to any other `Hashable`
    instances.This will result to `True` if both `Hashable` instances have the same `hash` property.
    * ** \_\_hash\_\_ **: Using set() makes this a killing feature. You can easily do intersection and union of sets of hashes


The _two_ properties(`hash` and `binary`) are instance methods turned into _properties_ through the python **@property**
_decorator_.In addition,each new **property** has a complimentary **@setter** method that  protects  `hash` or the `
binary` property from changing values when they are assigned a new value.


> Any _class_ subclassing from  `Hashable` will implement the above outlined interface in
> _addition_ to any extra features the class might also provide.

Here is an example of a `Hashable` instance being initiated through the regular **__init__** method:

    #!python
    #Represents a move on cell 5 by player 1.
    Move(cell=5,player=1)

An another example of  creating the same `Hashable` instance but this time through
the alternative construction **from_hash** _class method_:

    #!python
    #Represents a move on cell 5 by player 1, using a hash.
    Move.from_hash(hash=8192)


"""

import abc

class Hashable(object):

    __metaclass__ = abc.ABCMeta


    def __eq__(self,hashable):
        if not isinstance(hashable,Hashable):
            return False

        return self.hash == hashable.hash

    def __hash__(self):
        return self.hash

    @property
    @abc.abstractmethod
    def hash(self):

        """
            A hash representation of the current `Hashable` instance. An `int` or
            a `long` type must be returned.
        """

    @hash.setter
    @abc.abstractmethod
    def hash(self,value):

        """
            This method should really be left with a pass and nothing else.
            Changing the hash value of a `Hashable` object after it has been
            created will create undefined behaviour when other objects
            operate on them.
        """

    @property
    @abc.abstractmethod
    def binary(self):

        """
            This should return an string consisting of 0's and 1's representing
            the binary value of the `Hashable` instance.

                #Example of turning a hash into a binary str of 0's and 1's
                bits_size_of_hash = 27
                hash = 4
                bin(hash)[2:].zfill(bits_size_of_hash)

        """

    @binary.setter
    @abc.abstractmethod
    def binary(self,value):

        """
            This method should really be left with a pass and nothing else.
            Changing the binary value of a `Hashable` object after it has been
            created will create undefined behaviour when other objects
            operate on them.
        """

    @classmethod
    @abc.abstractmethod
    def from_hash(cls,hash):

        """
            Alternative method for constructing a `Hashable` instance. All `Hashable`
            instances must have a method for constructing an instance from a *hash*.
            Either the **__init__** method or the **from_hash** method must implement
            this needed feature.
        """


