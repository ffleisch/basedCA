import imageio
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

import kernel_collection

kernel=kernel_collection.kernel


def step(state,kernel,modul):
    counts = np.round(scipy.signal.fftconvolve(state, kernel))
    return counts % modul

def createBaseN(kernel,modul, iters):
    base=[]
    base.append(np.array(kernel))
    for i in range(iters-1):
        kernel_new=step(base[-1],base[-1],modul)
        for j in range(1,modul-1):
            kernel_new=step(base[-1],kernel_new,modul)
        base.append(kernel_new)
    return base


all_bases=[]
for i in range(2,10):
    base=createBaseN(kernel,i,4)
    all_bases.append(base)
    for j,b in enumerate(base):
        if(j==0):
            continue
        imageio.imwrite("./base_tests/mod%d_pow%d.png"%(i,j+1),b)

res=step(all_bases[1][1],all_bases[1][1],6)

fig,axs=plt.subplots(1,2)


axs[0].imshow(res,cmap="gray")
axs[1].imshow(all_bases[4][1],cmap="gray")
plt.show()

