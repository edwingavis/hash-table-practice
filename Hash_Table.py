# Practice: Markov models and hash tables
# Edwin Gavis


TOO_FULL = 0.5
GROWTH_RATIO = 2


class Hash_Table:

    def __init__(self,cells,defval):
        '''
        Construct a bnew hash table with a fixed number of cells equal to the
        parameter "cells", and which yields the value defval upon a lookup to a
        key that has not previously been inserted
        '''
        self.table = [None] * cells
        self.defval = defval
        self.count = 0

    def lookup(self,key):
        '''
        Retrieve the value associated with the specified key in the hash table,
        or return the default value if it has not previously been inserted.
        '''
        rv = self.table[self.probe(key)]
        if not rv:
            return self.defval
        return rv[1]

    def update(self,key,val):
        '''
        Change the value associated with key "key" to value "val".
        If "key" is not currently present in the hash table,  insert it with
        value "val".
        '''
        i = self.probe(key)
        if not self.table[i]:
            self.count += 1
        self.table[i] = (key, val)
        if self.count / len(self.table) > TOO_FULL: 
            self.grow_table()

    def probe(self,key):
        '''
        Hash the key and return the resulting index found via linear probing.
        '''
        rv = self.get_hash(key)
        while self.table[rv] and self.table[rv][0] != key:
            rv += 1
            if rv == len(self.table):
                rv = 0
        return rv

    def get_hash(self,key):
        '''
        Returns integer hash for the key.
        '''
        rv = 0
        for letter in key:
            rv = (rv * 37 + ord(letter)) % len(self.table)
        return rv

    def grow_table(self):
        '''
        Grows the table and rehashes existing keys and values 
        into the larger table.
        '''
        rehash = self.table
        new_length = len(self.table) * GROWTH_RATIO
        self.__init__(new_length, self.defval)
        for cell in rehash:
            if cell:
                self.update(cell[0], cell[1])

