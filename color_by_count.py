import os

import imageio
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from skimage import measure
from matplotlib import colors
from PIL import Image
Image.MAX_IMAGE_PIXELS=None


path="./results/43.png"

#path="./results_sparse_conv/1197.png"
img=imageio.imread_v2(path)




plt.imshow(img)
plt.show()

'''fig, ax = plt.subplots()
ax.set_aspect("equal")
#ax.imshow(img)
contours=measure.find_contours(img,127)
for contour in contours:
      #ax.plot(contour[:, 1], contour[:, 0], linewidth=1,c="k")
      ax.fill(contour[:, 1], contour[:, 0],c="k")
plt.show()#'''


mask=[[0,1,0],
      [1,1,1],
      [0,1,0]]

labels, num_features=ndimage.label(img,structure=mask)

plt.imshow(labels)
plt.show()

hist,_=np.histogram(labels,num_features+1)
hist[0]=0
#plt.plot(hist)
#plt.show()



unique_sizes,unique_inverse=np.unique(hist,return_inverse=True)





#colored=colors[hist[labels]%len(colors)]
sizes=unique_sizes[unique_inverse[labels]]

bw_colors=np.random.rand(len(unique_sizes))
bw_colors[0]=0

unique_indices=unique_inverse[labels]

#img_colored=bw_colors[unique_indices]


mycolors=[]
n_colors=len(unique_indices)
mycolors.append((0, 0, 0))
for i in range(n_colors):
      #mycolors.append(randomColor())
      #mycolors.append(colors.hsv_to_rgb((i/n_colors,np.random.rand(),1)))

      mycolors.append(colors.hsv_to_rgb((np.random.rand(),np.random.rand(),np.random.rand()*0.2+0.8)))
#img_colored=np.zeros((img.shape[0],img.shape[1],3))

cmap=matplotlib.colors.ListedColormap(mycolors)

img_colored=cmap(plt.Normalize()(unique_indices))

plt.imshow(img_colored)
plt.show()

out_path=os.path.join("results_count_colored",os.path.splitext(os.path.basename(path))[0])+"_%03d"%np.random.randint(0,100)+".png"
print(out_path)
imageio.imwrite(out_path,img_colored)

