import numpy
import numpy as np
import scipy.signal
import imageio
from scipy import signal

from matplotlib import pyplot as plt, colors

board_size=1

modul=2


array=np.zeros((board_size,board_size),dtype=int)

#init=np.array([[0,1,0],[1,1,1],[0,1,0]])

init=np.ones((1,1))
#init[1:-1,1:-1]=0
print(init)

init_w=init.shape[0]
init_h=init.shape[1]

array[int(board_size/2-init_w/2):int(board_size/2-init_w/2)+init_w,int(board_size/2-init_h/2):int(board_size/2-init_h/2)+init_h]=init





#state_table=np.array([0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],dtype=int)



#modul=np.random.randint(2,15)
#state_table=np.random.randint(0,2,modul)


#k_size=21
#kernel=np.ones((2*k_size+1,2*k_size+1),dtype=int)


'''kernel=[[0,0,0,0,0,0,0],
        [0,0,1,1,1,0,0],
        [0,0,0,0,1,1,0],
        [0,0,1,1,1,1,0],
        [0,0,1,1,1,1,0],
        [0,0,1,0,1,0,0],
        [0,0,0,0,0,0,0],
       ]'''


'''kernel=[[0,0,0,0,1,0,0,0,0],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,0,1,0,0,0,0],
        [1,1,1,1,1,1,1,1,1],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,0,1,0,0,0,0]

        ]'''

kernel=[[1,0,0,1,0,0,1],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [1,1,1,1,1,1,1],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [1,0,0,1,0,0,1],

        ]
'''kernel=imageio.imread_v2("kernels/Kernel_cross9x9_4.png")/255'''


plt.imshow(kernel)
plt.show()
print(modul,kernel)


#cmap = colors.ListedColormap(['black',colors.CSS4_COLORS["tomato"],colors.CSS4_COLORS["palegreen"],colors.CSS4_COLORS["slateblue"]])
cmap = colors.ListedColormap(['black',"white"])

#color_list=["black"]
#color_list.extend(colors.CSS4_COLORS)
#cmap = colors.ListedColormap(color_list)

#plt.ion()

for i in range(128):

    #plt.clf()

    counts=np.round(scipy.signal.fftconvolve(array,kernel))#,boundary="fill")#,mode="same",boundary="wrap")

    #plt.imshow(counts)
    #plt.show()

    #counts=counts.astype(int)
    array=counts%modul



    imageio.imwrite("./results/"+str(i+1)+".png",array)
    #plt.imshow(array,cmap=cmap,interpolation="none")

    #plt.pause(0.01)
    #plt.draw()
    print(i)
    #plt.show()

imageio.imwrite("./results/final.bmp",array)

plt.ioff()
plt.clf()
plt.imshow(array,cmap=cmap,interpolation="none")
plt.show()