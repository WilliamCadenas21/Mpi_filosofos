from mpi4py import MPI 
from texttable import Texttable
import random
import numpy as np 
import time

comm = MPI.COMM_WORLD 
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    t = Texttable()
    typeOfPhilosopher = []
    info1 = []
    info2 = []

    for i in range(0,size-1): 
        typeOfPhilosopher.append('Filosofo ' + str(i) + ' Amigable') 
        info1.append('0 | x')
        info2.append('x')

    for i in list(range(2)):
        randNumber = random.randrange(0,size-1)
        typeOfPhilosopher[randNumber] = 'Filosofo ' + str(randNumber) + ' Ambicioso'
    

    t.add_rows([typeOfPhilosopher,info1,info2])

    for i in range(0,7):
        time.sleep(1)
        print('tabla',i)
        print (t.draw())
        

        

else:
    print('acabo de inciar ',rank-1)    
    #while True :
    rand = random.randrange(7,10)
        #time.sleep(rand)
    #    print('soy el proceso ',rank,' y acabo de desertar')
    print('rand: ', rand)
