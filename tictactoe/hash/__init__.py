
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

        """This should return an int as a hash representation for the
            hashable object.
        """

    @hash.setter
    @abc.abstractmethod
    def hash(self,value):

        """ This method should really be left with a pass and nothing else.
            Changing the hash value of a hashable object after it has been
            created will create undefined behaviour when other objects
            operate on them.
        """

    @property
    @abc.abstractmethod
    def binary(self):

        """
            This should return an string consisting of 0's and 1's representing
            the binary value of the hashable object.

            Example : bin(hash)[2:].zfill(bits_size_of_hash)
        """

    @binary.setter
    @abc.abstractmethod
    def binary(self,value):

        """
            This method should really be left with a pass and nothing else.
            Changing the binary value of a hashable object after it has been
            created will create undefined behaviour when other objects
            operate on them.
        """

    @classmethod
    @abc.abstractmethod
    def from_hash(cls,hash):

        """
            All hashable classes inheriting this class MUST implement from_hash method,
            which becomes the DEFAULT method for instantiating new Hashable instances
            or subclasses
        """


