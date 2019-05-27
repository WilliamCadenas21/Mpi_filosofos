from mpi4py import MPI 
from texttable import Texttable
import random
import numpy as np 
import time
import sys

comm = MPI.COMM_WORLD 
rank = comm.Get_rank()
n = comm.Get_size()

##SATATES
# 0 THINKING
# 1 HUNGRY
# 2 EATING 

def think(rank):
    rand = random.randrange(7,10)
    print('soy el proceso ',rank,'y voy a dormir ', rand)
    sys.stdout.flush()
    time.sleep(rand)
    print('soy el proceso ',rank,' y acabo de desertar')
    sys.stdout.flush()

def take_forks(rank):
    down_mutex(rank) # enter critical region
    state[rank] = 1
    test(rank)
    up_mutex()

def test(rank):
    n=1

def down_mutex(rank):
    while True: 
        if mutex[0] == 1:
            mutex[0] = 0 #bloquea el mutex 
            print('rank ',rank,'TERMINE DE ESPERAR')
            sys.stdout.flush()
            break

def up_mutex():
    mutex[0] = 1

## ALL THIS CODE IS FOR THE MUTAL INFO

# create a shared array of size 1000 elements of type double
size = 1000 
itemsize = MPI.DOUBLE.Get_size() 
if rank == 0: 
    nbytes = size * itemsize 
else: 
    nbytes = 0
# on rank 0, create the shared block
# on rank 1 get a handle to it (known as a window in MPI speak)
win = MPI.Win.Allocate_shared(nbytes, itemsize, comm=comm) 
# create a numpy array whose data points to the shared mem
buf, itemsize = win.Shared_query(0) 
assert itemsize == MPI.DOUBLE.Get_size() 
mutex = np.ndarray(buffer=buf, dtype='d', shape=(size,))
state = np.ndarray(buffer=buf, dtype='d', shape=(size,))
semaforo = np.ndarray(buffer=buf, dtype='d', shape=(size,))
forks1 = np.ndarray(buffer=buf, dtype='d', shape=(size,))
leftFork1 = np.ndarray(buffer=buf, dtype='d', shape=(size,))
##FINISH


if rank == 0:
    t = Texttable()
    typeOfPhilosopher = []
    forks = []
    leftFork = []

    for i in range(0,n-1): 
        typeOfPhilosopher.append('Filosofo ' + str(i) + ' Amigable') 
        forks.append('0 | x')
        leftFork.append('x')

    for i in list(range(2)):
        randNumber = random.randrange(0,n-1)
        typeOfPhilosopher[randNumber] = 'Filosofo ' + str(randNumber) + ' Ambicioso'
    

    t.add_rows([typeOfPhilosopher,forks,leftFork])

    count = 0
    mutex[0] = 1 # initialize mutex availabel

    while True:
        count += 1
        time.sleep(1)
        print('table: ',count)
        #print(typeOfPhilosopher)
        #print(forks)
        #print(leftFork)
        print (t.draw())
        #print(mutex[:1])
        sys.stdout.flush()
        #print(state[:5])
        #sys.stdout.flush()

else:
    #print('acabo de inciar ',rank)    
    while True :
        #PENSANDO
        think(rank)
        take_forks(rank)



