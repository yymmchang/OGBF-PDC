import hashlib
import random

class Bloom:
    def __init__(self, inputArray, m=512, lam=16):
        self.inputArray = inputArray
        self.m = m
        self.lam = lam
        self.garbledBloomArray = [None for _ in range(self.m)]
        self.bloomArray = [0 for _ in range(self.m)]

    def getLambda(self):
        return self.lam

    def getInput(self):
        return self.inputArray

    def getGarbledBloom(self):
        return self.garbledBloomArray

    def getBloom(self):
        return self.bloomArray

    def _hash_indices(self, element):
        h = [hashlib.sha1(), hashlib.sha384(), hashlib.sha512()]
        indices = []
        for i in range(len(h)):
            val = h[i].copy()
            val.update(str(element).encode())
            j = int(val.hexdigest(), 16) % self.m
            indices.append(j)
        return indices

    def generateBloom(self):
        for element in self.inputArray:
            for j in self._hash_indices(element):
                self.bloomArray[j] = 1

    def generateGarbledBloom(self):
        for element in self.inputArray:
            indices = self._hash_indices(element)
            emptySlot = -1
            finalShare = self._element_share(element)
            for j in indices:
                if self.garbledBloomArray[j] is None:
                    if emptySlot == -1:
                        emptySlot = j
                    else:
                        share = random.getrandbits(self.lam)
                        self.garbledBloomArray[j] = share
                        finalShare ^= share
                else:
                    finalShare ^= self.garbledBloomArray[j]
            self.garbledBloomArray[emptySlot] = finalShare

        for i in range(self.m):
            if self.garbledBloomArray[i] is None:
                self.garbledBloomArray[i] = random.getrandbits(self.lam)

    def _element_share(self, element):
        h = hashlib.sha256()
        h.update(str(element).encode())
        return int.from_bytes(h.digest(), 'big') & ((1 << self.lam) - 1)

    def queryBloom(self, x):
        for j in self._hash_indices(x):
            if self.bloomArray[j] == 0:
                return False
        return True

    def queryGarbled(self, x, GBF):
        if len(GBF) != self.m:
            raise ValueError(f"GBF length mismatch: expected {self.m}, got {len(GBF)}")
        recovered = 0
        for j in self._hash_indices(x):
            recovered ^= GBF[j]
        return recovered == self._element_share(x)

    def generateIntersection(self, GBF):
        GBFint = [None for _ in range(self.m)]
        for i in range(self.m):
            GBFint[i] = GBF[i] if self.bloomArray[i] else random.getrandbits(self.lam)
        return GBFint