import os

f= open('seedlist.txt','r')
seed=f.readline()
while (seed):
    print(seed)
    seed=f.readline()