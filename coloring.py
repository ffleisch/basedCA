import os.path
import random

import matplotlib.colors
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
import imageio
from sklearn import cluster


path_str="results/179.png" # 429


n_clusters=20
n = 3
#path_str = "results_skipiters/2031.png"

img = imageio.imread_v2(path_str)

img=np.pad(img,((5,5),(5,5)))

#plt.imshow(img)

#plt.show()

# def array_to_key(arr):
#    return hash(arr)


n_half = int(n / 2)
histogram = {}
patches = {}
img_padded=np.pad(img,((n_half,n_half),(n_half,n_half)))

for i in range(0, img.shape[0]-1):
    for j in range(0, img.shape[1]-1):

        arr = img_padded[i:i + n, j:j + n]
        #if arr.shape[0]<n or arr.shape[1]<n:
        #    continue
        if arr[n_half][n_half]==0:
            continue

        hash_val = hash(arr.data.tobytes())

        if not hash_val in histogram:
            histogram[hash_val] = 0
            patches[hash_val] = arr
        histogram[hash_val] += 1

cleaned_histogram = {}
translation={}
for (key, value) in histogram.items():
    new_key = key

    arr = patches[key]
    for j in range(2):
        for i in range(3):
            arr=np.rot90(arr)
            new_key = min(new_key, hash(arr.data.tobytes()))
        if(j==0):
            arr=np.fliplr(patches[key])
            new_key = min(new_key, hash(arr.data.tobytes()))



    if not new_key in cleaned_histogram:
        cleaned_histogram[new_key] = value
    if not key in translation:
        translation[key]=new_key

    cleaned_histogram[new_key] += value

histogram_list = list(cleaned_histogram.items())

histogram_list.sort(key=lambda x: -x[1])




cmap={}
num=1



def randomColor():
    return (random.random(),random.random(),random.random())
print(len(cleaned_histogram))
for (key,value) in histogram_list:
    l=len(histogram_list)
    cmap[key]=(.1 + .9 * num / l, .1 + .9 * num / l, .1 + .9 * num / l)
    num+=1


img_hashes=np.zeros_like(img,dtype=np.int64)



for i in range(0, img_hashes.shape[0]):
    for j in range(0, img_hashes.shape[1]):
        arr = img_padded[i:i + n, j:j + n]
        if arr[n_half][n_half]==0:
            continue
        hash_val = translation[hash(arr.data.tobytes())]
        #print(colors[hash_val])
        img_hashes[i][j]=hash_val



#plt.imshow(img_hashes)
#plt.show()

neigh_matrix=np.zeros((len(cleaned_histogram)+1,len(cleaned_histogram)+1))

index_dict={}
index_dict[0]=0
num=1
for hash_val in cleaned_histogram:
    index_dict[hash_val]=num
    num+=1

print("counting neighbours")
for i in range(0,img_hashes.shape[0]):
    for j in range(0,img_hashes.shape[1]):
        for m in (-4,-3,-2,-1,0,1,2,3,4):
            for n in (-4,-3,-2,-1,0,1,2,3,4):
                if(m==n==0):
                    continue
                x=i+m
                y=j+n
                if not (x>=0 and x<img_hashes.shape[0]):
                    continue
                if not (y>=0 and y<img_hashes.shape[1]):
                    continue
                neigh_matrix[index_dict[img_hashes[i][j]]][index_dict[img_hashes[x][y]]]+=1

neigh_matrix=neigh_matrix[1:,1:]

neigh_matrix=np.exp((1-neigh_matrix/np.amax(neigh_matrix)**2),dtype=float)
plt.imshow(neigh_matrix)
plt.show()

print("clustering")

clustering=cluster.spectral_clustering(neigh_matrix, n_clusters=n_clusters)

cluster_plus_zero=np.zeros(clustering.shape[0]+1)
cluster_plus_zero[0]=0
cluster_plus_zero[1:]=clustering+1

img_clustered=np.vectorize(lambda x:index_dict[x],otypes=[int])(img_hashes)

mycolors=[]
mycolors.append((0, 0, 0))
for i in range(clustering.shape[0]):
    #mycolors.append(randomColor())
    mycolors.append(colors.hsv_to_rgb((i/clustering.shape[0],0.7,1)))
#img_colored=np.zeros((img.shape[0],img.shape[1],3))

cmap=matplotlib.colors.ListedColormap(mycolors)

img_colored=cmap(plt.Normalize()(cluster_plus_zero[img_clustered]))


plt.imshow(img_colored)
plt.show()
plt.imshow(cluster_plus_zero[img_clustered])
plt.show()

out_path=os.path.join("results_colored",os.path.splitext(os.path.basename(path_str))[0])+"_%03d"%random.randint(0,100)+".png"
print(out_path)
imageio.imwrite(out_path,img_colored)

print("done")

'''for (hash_val, num) in histogram_list:
    print(patches[hash_val], num)
    plt.imshow(patches[hash_val], cmap="gray")
    plt.show()'''
#print(histogram)
