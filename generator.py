'''
Created on 08-Dec-2015

@author: pawan
'''

from Crypto.Random import random

def modifiedPower(n, m, mod):
    """Efficient modular exponentiation: (n ** m) % mod"""
    result = 1
    n = n % mod
    while m > 0:
        if m % 2 == 1:
            result = (result * n) % mod
        n = (n * n) % mod
        m = m // 2
    return result


def euclid(n, m):
    if m == 0:
        return n, 1, 0
    else:
        g, a, b = euclid(m, n % m)
        return g, b, a - (n // m) * b

def millerRabin(p):
    i=0
    while (p > (1<<i)):
        i+=1
    for k in range(0,10):
        n=random.randrange(1<<i)
        while(euclid(n,p)[0]!=1):
            n=random.randrange(1<<i)
        if modifiedPower(n,(p-1),p) != 1:
            return False
    
    return True

def generate_prime():
    while 1:
        q=random.randrange(1<<512)
        if millerRabin(q):
            break
    while 1:
        k=random.randrange(1<<10)
        if millerRabin(k*q+1):
            p=q*k+1;
            break
    while 1:
        h=random.randrange(2,p)
        if modifiedPower(h,(p-1)/q,p)!=1:
            g=modifiedPower(h,(p-1)/q,p)
            break
    
    return g,p,q
