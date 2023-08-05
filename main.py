import time

import numpy as np
import scipy.signal
import imageio
from matplotlib import pyplot as plt

import kernel_collection

board_size=1

modul=2 # modul to be applied after each step

state=np.ones((1, 1)) #inital state

kernel=kernel_collection.kernel #kernel for convolution

print(modul,kernel)

time_start = time.time()
for i in range(512):

    counts=np.round(scipy.signal.fftconvolve(state, kernel))
    state= counts % modul

    print(i)
    imageio.imwrite("./results/" + str(i+1) +".png", state)

    #plt.imshow(state,cmap=cmap,interpolation="none")
    #plt.show()

time_end = time.time()
print("done in %f seconds" % (time_end - time_start))

imageio.imwrite("./results/final.bmp", state)

plt.imshow(state, cmap="gray", interpolation="none")
plt.show()