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

##SATATES
# 0 THINKING
# 1 HUNGRY
# 2 EATING 

def think(pos):
    state[pos] = 0
    rand = random.randrange(7,10)
    print('soy el proceso ',pos,'y voy a pensar por ', rand)
    sys.stdout.flush()
    time.sleep(rand)
    print('soy el proceso ',pos,' tengo hambre')
    sys.stdout.flush()

def take_forks(pos):
    down_mutex(pos) # enter critical region
    #print('rank ',rank,'TERMINE DE ESPERAR')
    #sys.stdout.flush()
    #time.sleep(5)
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
                    break
                elif not ceroIntetos:
                    break
                else:    
                    rand = random.randrange(5,15)
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
                    break 


def eat(pos):
    if (forks1[pos] == 2):
        print('soy ',pos,' y voy a comer !!!')
        sys.stdout.flush()
        state[pos] = 2 #comiendo
        rand = random.randrange(2,5)
        time.sleep(rand)
        
    else:
        print('soy ',pos,' y no pude comer')
        sys.stdout.flush()    

def put_forks(pos):
    leftFork1[pos] = 0
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
typePhilo = np.ndarray(buffer=buf, dtype='d', shape=(size,))
typePhilo = typePhilo[:numberOfPhilosopher]
state = np.ndarray(buffer=buf, dtype='d', shape=(size,))
state = state[:numberOfPhilosopher]
forks1 = np.ndarray(buffer=buf, dtype='d', shape=(size,))
forks1 = forks1[:numberOfPhilosopher]
leftFork1 = np.ndarray(buffer=buf, dtype='d', shape=(size,))
leftFork1 = leftFork1[:numberOfPhilosopher]
##FINISH


if rank == 0:
    t = Texttable()
    typeOfPhilosopher = []

    for i in list(range(0,numberOfPhilosopher)): 
        typeOfPhilosopher.append('Filosofo ' + str(i) + ' Amigable')
        typePhilo[i] = 1 #amigable
        #state[i] = 0
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
    
    

comm.barrier()
print('todos llegaron hasta aqui')
sys.stdout.flush()
mutex[0] = 1 # initialize mutex availabel

if rank == 0:
    count = 0
    t = Texttable()
    t.add_rows([typeOfPhilosopher,state,typePhilo])
    print('table: ',count)
    print (t.draw())
    while True:
        
        count += 1
        time.sleep(1)
        #print(typeOfPhilosopher)
        #print(forks1)
        #print(leftFork1)
        #print(state[:5])
        print(mutex)
        sys.stdout.flush()
        print('state:',state)
        sys.stdout.flush()        
        print('type:',typePhilo)
        sys.stdout.flush()
        
        #t = Texttable()
        #t.add_rows([typeOfPhilosopher,state])
        #print('table: ',count)
        #print (t.draw())
        sys.stdout.flush()
        
else:
    #print('Filosofo numero ',rank, 'acaba de despertar')    
    pos = rank -1
    while True :
        #PENSANDO
        think(pos)
        print('soy',pos,' voy intentar tomar cubiertos')
        take_forks(pos)
        eat(pos)
        put_forks(pos)



