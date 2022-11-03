
import numpy as np
import scipy.signal
import imageio
from matplotlib import pyplot as plt, colors


modul=2

init=np.ones((1,1))

kernel=[[1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,1,0,0,0,1,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,1,0,0,0,1,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1],

        ]#'''

#kernel=[[1,1,0],
#        [1,0,1],
#        [0,1,1]]

'''kernel=[[0,0,0,0,0,0,0],
        [0,0,1,1,1,0,0],
        [0,0,0,0,1,1,0],
        [0,0,1,1,1,1,0],
        [0,0,1,1,1,1,0],
        [0,0,1,0,1,0,0],
        [0,0,0,0,0,0,0],
       ]#'''

def step(state,kernel):
        counts = np.round(scipy.signal.fftconvolve(state, kernel))
        return counts % modul


def createBase(kernel, iters):
        base=[]
        base.append(np.array(kernel))
        for i in range(iters-1):
                kernel_new=step(base[-1],base[-1])
                base.append(kernel_new)

        return base

n=599
print(n)

base=createBase(kernel,int(np.ceil(np.log2(n))))
#for b in base:
#        plt.imshow(b,cmap="gray")
#        plt.show()

i=1
num=0
state=init.copy()
while i<=n:
        print(i,i&n)
        if i&n!=0:
                state=step(state,base[num])
        i=i<<1
        num+=1

plt.imshow(state,cmap="gray")
plt.show()
