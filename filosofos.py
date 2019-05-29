from mpi4py import MPI 
from texttable import Texttable
import random
import numpy as np 
import time
import sys

##CODE MADE BY WILLIAM CADENAS :D

comm = MPI.COMM_WORLD 
rank = comm.Get_rank()
n = comm.Get_size()
numberOfPhilosopher = n-1
typeOfPhilosopher = []

k = int(sys.argv[1])

##SATATES
# 0 THINKING
# 1 HUNGRY
# 2 EATING 

##Forks1
# 0 no tiene cuebiertos
# 1 tiene el izq
# 2 tiene los dos cuebiertos 

def think(pos):
    rand = random.randrange(7,10)
    time.sleep(rand)

def take_forks(pos):
    state[pos] = 1 # Hungry
    test(pos) 

def test(pos):
    right = (pos+1) % (numberOfPhilosopher)
            
    if (typePhilo[pos] == 1): #amigable
        ceroIntetos = True
        while True:  
            if (leftFork1[pos] == 0):
                leftFork1[pos]= 1
                forks1[pos] = 1

            if (forks1[pos] == 1):
                if (leftFork1[right] == 0):
                    forks1[pos] = 2
                    leftFork1[right] = 1
                    break
                elif not ceroIntetos:
                    break
                else:    
                    rand = random.randrange(5,15)
                    time.sleep(rand) #tiempo de espera
                    ceroIntetos = False
    else:    
        while True: # ambiciosos
            if (leftFork1[pos]==0):
                leftFork1[pos]= 1
                forks1[pos] = 1
            if (forks1[pos] == 1):
                if (leftFork1[right] == 0):
                    forks1[pos] = 2
                    leftFork1[right] = 1
                    break 

def eat(pos):
    if (forks1[pos] == 2):
        state[pos] = 2 #comiendo

        rand = random.randrange(2,5)
        time.sleep(rand) # comiendo !!!!!!!!!!!!!!

        kPro[pos] = kPro[pos] - 1
        state[pos] = 0 #regresa a pensar

def put_forks(pos):
    if state[pos] == 1: #todavia tiene hambre
        forks1[pos] = 0
        leftFork1[pos] = 0
    elif state[pos] == 0:  #ya comio    
        right = (pos+1)%(numberOfPhilosopher)
        leftFork1[pos] = 0
        leftFork1[right] = 0
        forks1[pos] = 0

## ALL THIS CODE IS FOR THE MUTAL INFO

# create a shared array of size 1000 elements of type double
size = 1000 
itemsize = MPI.DOUBLE.Get_size() 
#print('itemsize', itemsize)
if rank == 0:
    print('aguarde un momento, estamos inicializando los procesos...')
    sys.stdout.flush() 
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
mutex = mutex[:1]

state = np.ndarray(buffer=buf, dtype='d', shape=(size,))
state = state[1:numberOfPhilosopher+1]
init = numberOfPhilosopher+1

forks1 = np.ndarray(buffer=buf, dtype='d', shape=(size,))
forks1 = forks1[init:init+numberOfPhilosopher]
init = init+numberOfPhilosopher

leftFork1 = np.ndarray(buffer=buf, dtype='d', shape=(size,))
leftFork1 = leftFork1[init:init+numberOfPhilosopher]
init = init+numberOfPhilosopher

typePhilo = np.ndarray(buffer=buf, dtype='d', shape=(size,))
typePhilo = typePhilo[init:init+numberOfPhilosopher]
init = init+numberOfPhilosopher

kPro = np.ndarray(buffer=buf, dtype='d', shape=(size,))
kPro= kPro[init:init+numberOfPhilosopher]
##FINISH

if rank == 0:
    t = Texttable()

    for i in list(range(0,numberOfPhilosopher)): 
        typeOfPhilosopher.append('Filosofo ' + str(i) + ' Amigable')
        state[i] = 0 #think
        forks1[i] = 0 #cero cubiertos
        leftFork1[i] = 0 #
        typePhilo[i] = 1 #amigable
        kPro[i] = k

    ant=-1
    for i in list(range(2)):
        while True:
            randNumber = random.randrange(0,numberOfPhilosopher)
            if randNumber != ant:
                ant=randNumber
                typeOfPhilosopher[randNumber] = 'Filosofo ' + str(randNumber) + ' Ambicioso'
                typePhilo[randNumber] = 2 #ambicioso
                break        

if rank == 0:
    comm.barrier()
else:
    time.sleep(1)
    comm.barrier()

mutex[0] = 1# initialize mutex availabel

if rank == 0:
    countTable = 0
    sw = True
    while sw:
        countTable += 1
        time.sleep(1)
        showForks = []
        showLeftFork = []
        showState = []

        count = 0 #reset
        for i in list(range(0,numberOfPhilosopher)):
            if forks1[i] == 0:
                showForks.append('0 | 0')
            elif forks1[i] == 1:
                showForks.append('x | 0')   
            else:
                showForks.append('x | x') 

            if leftFork1[i] == 0:
                showLeftFork.append('libre') 
            else:        
                showLeftFork.append('ocupado')

            if state[i] == 0:
                showState.append('pensando')
            elif state[i] == 1:
                showState.append('hambriento')
            elif state[i] == 2:
                showState.append('COMIENDO')
            else:     
                showState.append('finalizo')
                count +=1

            if count == numberOfPhilosopher:
                sw = False    

        t = Texttable()
        t.add_rows([typeOfPhilosopher,showForks,showLeftFork,showState])
        print('table: ',countTable)
        print (t.draw())
        sys.stdout.flush()
    
    print('El programa a terminado')
    sys.stdout.flush()
else: #otros procesos 
    pos = rank -1 # rank > 1 son filosofos 
    while kPro[pos] != 0:
        think(pos)
        take_forks(pos)
        eat(pos)
        put_forks(pos)

    state[pos] = 4 # Finalizado   
