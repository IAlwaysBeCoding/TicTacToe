

from tictactoe.hash import Hashable

class HashTable(object):

    def __init__(self,table={}):

        if not isinstance(table, dict):
            raise TypeError(
                'table is not a valid dictionary instance.')


        for maybe_hashable in table:
            self.verify_hashable(hashable=table[maybe_hashable])

        self.table = table


    def __getitem__(self,key):

        return self.get(hash=key,silent=False)

    def __setitem__(self,key,hashable):
        self.verify_hashable(hashable)

        if key != hashable.hash:
            raise ValueError(
                'Key:{} is not the same hash as hashable hash:{}'.format(key,hashable.hash))

        self.table[key] = hashable


    def __delitem__(self,key):

        return self.delete(hash=key,silent=False)

    def get(self,hash,silent=True):

        if silent:
            return self._table.get(hash,None)

        return self.table[hash]

    def delete(self,hash,silent=True):

        hashable = self.get(hash,silent)
        if hashable is None:
            return hashable

        del self.table[hash]

        return True

    def add(self,hashable,silent=True):

        self.verify_hashable(hashable)
        self.table[hashable.hash] = hashable

        return True

    def verify_hashable(self,hashable):
        if not isinstance(hashable,Hashable):
            raise TypeError(
                'hashable is not a valid Hashable instance. Instead a : ' \
                '{} type was found'.format(type(hashable)))

