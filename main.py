import numpy as np
import scipy.signal
import imageio
from matplotlib import pyplot as plt, colors

import kernel_collection

board_size=1

modul=2



state=np.ones((1, 1))
#state[3:-3, 3:-3]=0
#print(state)

kernel=kernel_collection.kernel

#plt.imshow(kernel)
#plt.show()

print(modul,kernel)


#cmap = colors.ListedColormap(['black',colors.CSS4_COLORS["tomato"],colors.CSS4_COLORS["palegreen"],colors.CSS4_COLORS["slateblue"]])
cmap = colors.ListedColormap(['black',"white"])

#color_list=["black"]
#color_list.extend(colors.CSS4_COLORS)
#cmap = colors.ListedColormap(color_list)

#plt.ion()

for i in range(256):

    counts=np.round(scipy.signal.fftconvolve(state, kernel))
    state= counts % modul

    print(i)
    imageio.imwrite("./results/" + str(i+1) +".png", state)

    #plt.imshow(state,cmap=cmap,interpolation="none")
    #plt.pause(0.01)
    #plt.draw()
    #plt.show()

imageio.imwrite("./results/final.bmp", state)

plt.ioff()
plt.clf()
plt.imshow(state, cmap=cmap, interpolation="none")
plt.show()