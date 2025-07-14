'''
Created on 08-Dec-2015

@author: pawan
'''
import random
import socket
import hashlib
from generator import euclid, modifiedPower, euclid
import math

class OTRecv():

    def __init__(self,g,p,q):
        self.g = g
        self.p = p
        self.q = q
        self.s = socket.socket()
        self.makeConnection()

    def generateK(self):
        return random.randrange(self.q)
    
    def makeConnection(self):
        self.s.connect(('127.0.0.1', 3000))

    def randomOracle(self, x):
        return int(hashlib.sha256(str(x)).hexdigest(), base=16)
        
    def obliviouslyReceive(self, X,number_of_OT, lam):
        client_socket = self.s
        final = []
        k=random.randrange(1,self.q+1);
        for i in range(number_of_OT):
            print(f"i={i}, X[i]={X[i]}")
            if X[i] not in [0, 1]:
                print(f"Warning: X[{i}] is not 0 or 1: {X[i]}")
                X[i] = 0
            c=int(client_socket.recv(200))
            pk=list()
            #print pk
            pk.insert(X[i],modifiedPower(self.g,k,self.q))
            gcd=inv=-1
            while gcd != 1 and inv <= 0 :
                gcd,inv,ui = euclid(modifiedPower(self.g,k,self.q),self.q)
            pk.insert(1-X[i],(c*inv)%self.q)
            if not str(pk[0]).isdigit():
                print(f"Warning: pk[0] is not digit: {pk[0]}")
                pk[0] = 0
            client_socket.send(str(pk[0]).encode())
            gr=client_socket.recv(200)
            #print("Received gr:", gr)
            gr = gr.decode().strip()
            if not gr:
                raise Exception("Received empty gr from server")
            grk = modifiedPower(int(gr), k, self.q)
            M0=client_socket.recv(lam)
            M1=client_socket.recv(lam)
            E=[M0,M1]
            r_guess0=hashlib.sha512((str(grk)+str(X[i])).encode()).digest()
            f=str(r_guess0)* int(math.ceil(number_of_OT/len(r_guess0))+1)
            T=int(E[X[i]],2)^ord(f[i])
            final.append(T)
        return final
