from mpi4py import MPI 
from texttable import Texttable
import random
import numpy as np 
import time
import sys

comm = MPI.COMM_WORLD 
rank = comm.Get_rank()
n = comm.Get_size()
numberOfPhilosopher = n-1
typeOfPhilosopher = []

##SATATES
# 0 THINKING
# 1 HUNGRY
# 2 EATING 

def think(pos):
    rand = random.randrange(7,10)
    #print('soy el proceso ',pos,'y voy a pensar por ', rand)
    #sys.stdout.flush()
    time.sleep(rand)
    #print('soy el proceso ',pos,' tengo hambre')
    #sys.stdout.flush()

def take_forks(pos):
    down_mutex(pos) # enter critical region
    #print('----------------------------------------------------soy',pos,'INTENTARE TOMAR CUBIERTOS')
    #sys.stdout.flush()
    state[pos] = 1 # Hungry
    test(pos) 
    up_mutex()

def test(pos):
    right = (pos+1)%(numberOfPhilosopher)
    if (typePhilo[pos] == 1):
        ceroIntetos = True
        while True:  
            if (leftFork1[pos]==0):
                leftFork1[pos]= 1
                forks1[pos] = 1
            if (forks1[pos] == 1):
                if (leftFork1[right]==0):
                    forks1[pos] = 2
                    leftFork1[right] = 1
                    break
                elif not ceroIntetos:
                    break
                else:    
                    rand = random.randrange(5,15)
                    #print('----------------------------------------------------soy',pos,'INTENTARE TOMAR CUBIERTO DERECHO DENTRO DE', rand)
                    #sys.stdout.flush()
                    time.sleep(rand)
                    ceroIntetos = False
    else:    
        while True:  
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
        #print('--------------------------------------------------------------soy ',pos,' y voy a comer !!!')
        #sys.stdout.flush()
        state[pos] = 2 #comiendo
        for j in list(range(0,int(kPro[0]))):
            rand = random.randrange(2,5)
            time.sleep(rand)
            #print('---------------------------------------------------------- soy',pos, 'termine el trabajo ',j)
            #sys.stdout.flush()
        state[pos] = 0 #se va a pensar
        #print('---------------------------------------------------------- soy',pos, 'y acabo de terminar de comer')
        #sys.stdout.flush()
    #else:
        #print('--------------------------------------------------------------soy ',pos,' y no pude comer asi que ire a pensar con hambre')
        #sys.stdout.flush()  
        #se va a pensar pero sigue con hambre 
        

def put_forks(pos):
    if state[pos] == 1: #todavia tiene hambre
        forks1[pos] = 0
        leftFork1[pos] = 0
    elif state[pos] == 0:    
        right = (pos+1)%(numberOfPhilosopher)
        leftFork1[pos] = 0
        leftFork1[right] = 0
        forks1[pos] = 0

def down_mutex(pos):
    while True: 
        if mutex[0] == 1:
            mutex[0] = 0 #bloquea el mutex 
            break

def up_mutex():
    mutex[0] = 1

## ALL THIS CODE IS FOR THE MUTAL INFO

# create a shared array of size 1000 elements of type double
size = 1000 
itemsize = MPI.DOUBLE.Get_size() 
#print('itemsize', itemsize)
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
kPro= kPro[init:init+1]
##FINISH


if rank == 0:
    t = Texttable()

    for i in list(range(0,numberOfPhilosopher)): 
        typeOfPhilosopher.append('Filosofo ' + str(i) + ' Amigable')
        state[i] = 0
        forks1[i] = 0
        leftFork1[i] = 0
        typePhilo[i] = 1 #amigable
        #forks.append('0 | x')
        #leftFork.append('x')

    ant=-1
    for i in list(range(2)):
        while True:
            randNumber = random.randrange(0,numberOfPhilosopher)
            if randNumber != ant:
                ant=randNumber
                typeOfPhilosopher[randNumber] = 'Filosofo ' + str(randNumber) + ' Ambicioso'
                typePhilo[randNumber] = 2 #ambicioso
                break

    print('digite el k para los filosofos:')
    kPro[0] = input()          


if rank == 0:
    comm.barrier()
else:
    time.sleep(1)
    comm.barrier()

mutex[0] = 1# initialize mutex availabel

if rank == 0:
    count = 0
    while True:
        count += 1
        time.sleep(1)
        showForks = []
        showLeftFork = []
        showState = []

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
            else:
                showState.append('COMIENDO')


        t = Texttable()
        t.add_rows([typeOfPhilosopher,showForks,showLeftFork,showState])
        print('table: ',count)
        print (t.draw())
        sys.stdout.flush()
        
else:  
    pos = rank -1
    #K= input()
    while True :
        think(pos)
        #print('soy',pos,'voy intentar tomar cubiertos')
        take_forks(pos)
        eat(pos)
        put_forks(pos)
