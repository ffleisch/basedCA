import cv2
import imageio
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage import measure
import drawsvg as draw

path = "results/255.png"
#path = "results_sparse_conv/317.png"
#path = "results_skipiters/31.png"

img = imageio.imread_v2(path)

img = np.pad(img, ((1, 1), (1, 1)), mode="constant", constant_values=0)

'''ret, thresh = cv2.threshold(img, 127, 255, 0)

contours, hierarchy= cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow("yeet",img)
cv2.drawContours(img,contours,-1,(255,0,0),1)
cv2.waitKey(0)
for c,h in zip(contours,hierarchy):
    print(c)
#'''

plt.imshow(img)
plt.show()

#mask = [[0, 1, 0],
#        [1, 1, 1],
#        [0, 1, 0]]

#labels, num_features = ndimage.label(img, structure=mask)

# filled_polygons=[]
'''for i in range(num_features):
    comp=labels==i+1
    contours=measure.find_contours(comp)

    contour=np.concatenate(contours)
    filled_polygons.append(contour)
    if len(contours)>1:
        plt.imshow(comp)
        plt.plot(contour[:, 1], contour[:, 0], linewidth=1,c="r")
        plt.show()
        plt.fill(contour[:,0],contour[:,1],c="k")
        plt.gca().set_aspect("equal")
        plt.show()'''

# for c in filled_polygons:
#    plt.fill(c[:,0],c[:,1],c="k")
# plt.gca().set_aspect("equal")
# plt.show()


contours = measure.find_contours(img,level=128)

d = draw.Drawing(img.shape[0]-1, img.shape[1]-1, origin="top-left")
d.append(draw.Rectangle(0, 0, height='100%',width= '100%', rx=None, ry=None, fill='rgb(255,255,255)'))
path = draw.Path(fill_rule="evenodd", stroke="none", fill="black")
print("making svg path")

commandstr=[]

for i, c in enumerate(contours):
        commandstr.append("M%g,%g "%(c[0][0],c[0][1]))
        commandstr.extend(["L%g,%g "%(p[0],p[1]) for p in c[1:,:]])
        commandstr.append("Z")
        print("\r%d%%" % int(100 * i / len(contours)), end="")
commandstr="".join(commandstr)
path.append(commandstr)


'''for i, c in enumerate(contours):
    path.M(c[0, 0], c[0, 1])
    for x, y in c[1:, :]:
        path.L(x, y)
    path.Z()
    print("\r%d%%" % int(100 * i / len(contours)), end="")'''
print()
print("done making svg path")
d.append(path)

d.save_svg("test.svg")
print("saved svg")
#d.set_pixel_scale(4)
#d.save_png("test.png")
#print("saved png")