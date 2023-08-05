import hashlib
import logging
import math

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

# m = ceil((n * log(p)) / log(1 / pow(2, log(2))));


class Bloom:

    def __init__(self, bits, rounds, hasher=None):
        self.bits = bits
        self.bytes = int(bits / 8)
        if self.bytes * 8 != self.bits:
            raise ValueError('Need byte boundary bit value')
        self.rounds = rounds
        self.filter = [0] * self.bytes
        if hasher == None:
            logg.info('using default hasher (SHA256)')
            hasher = self.__hash
        self.hasher = self.set_hasher(hasher)


    def set_hasher(self, hasher):
        self.hasher = hasher


    def add(self, b):
        for i in range(self.rounds):
            salt = str(i)
            s = salt.encode('utf-8')
            z = self.__hash(b, s)
            r = int.from_bytes(z, byteorder='big')
            m = r % self.bits
            bytepos = math.floor(m / 8)
            bitpos = m % 8
            self.filter[bytepos] |= 1 << bitpos
            logg.debug('foo {} {}'.format(bytepos, bitpos))
        return m


    def check(self, b):
        for i in range(self.rounds):
            salt = str(i)
            s = salt.encode('utf-8')
            z = self.__hash(b, s)
            r = int.from_bytes(z, byteorder='big')
            m = r % self.bits
            bytepos = math.floor(m / 8)
            bitpos = m % 8
            if not self.filter[bytepos] & 1 << bitpos:
                return False
            return True


    def dump(self):
        return self.filter


    def __hash(self, b, s):
       logg.debug('hashing {} {}'.format(b.hex(), s.hex()))
       h = hashlib.sha256()
       h.update(b)
       h.update(s)
       return h.digest()
