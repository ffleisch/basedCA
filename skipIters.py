import math

import numpy as np
import scipy.signal
import imageio
from matplotlib import pyplot as plt, colors


modul=3

init=np.ones((1,1))

'''kernel=[[1,1,1,1,1,1,1,1,1],
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

'''kernel=[[0,1,1,0,1,1,0],
        [1,1,1,0,1,1,1],
        [1,1,1,0,1,1,1],
        [0,0,0,0,0,0,0],
        [1,1,1,0,1,1,1],
        [1,1,1,0,1,1,1],
        [0,1,1,0,1,1,0],
        ]#'''

kernel=[[0,0,1,0,0],
        [0,1,1,1,0],
        [1,1,0,1,1],
        [0,1,1,1,0],
        [0,0,1,0,0]]



def step(state,kernel):
        counts = np.round(scipy.signal.fftconvolve(state, kernel))
        return counts % modul


def createBase2(kernel, iters):
        base=[]
        base.append(np.array(kernel))
        for i in range(iters-1):
                kernel_new=step(base[-1],base[-1])
                base.append(kernel_new)

        return base

def createBaseN(kernel, iters):
        base=[]
        base.append(np.array(kernel))
        for i in range(iters-1):
                kernel_new=step(base[-1],base[-1])
                for j in range(1,modul-1):
                        kernel_new=step(base[-1],kernel_new)
                base.append(kernel_new)
        return base

#n=0b101111111

#n=(119<<5)+55


l=[1,2,2,2,1,1,2]
n=0
for i in l:
        n=n*modul+i


print(n)
name=str(n)
base=createBaseN(kernel,1+int(math.log(n,modul)))
print("base length: ",len(base))
#for b in base:
#        plt.imshow(b,cmap="gray")
#        plt.show()

i=1
state=init.copy()
num=0
while n>0:
        r=n%modul
        print(r,n,num)

        for i in range(r):
                #print("ye")
                state=step(state,base[num])

        #plt.imshow(state,cmap="gray")
        #plt.show()
        num+=1
        n=int(n/modul)


'''
i=1
num=0
state=init.copy()
while i<=n:
        print(i&n,state.shape,base[num].shape)
        if i&n!=0:
                state=step(state,base[num])
        i=i<<1
        num+=1
'''

print(state.shape)

print("saving")
imageio.imwrite("./results_skipiters/"+str(name)+".png",state)
print("done")

color_list=["black","white"]
#color_list.extend(colors.CSS4_COLORS)
cmap = colors.ListedColormap(color_list)

plt.imshow(state,cmap=cmap)
plt.show()
