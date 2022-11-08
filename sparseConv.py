import math
import time

import imageio
import numpy as np
import scipy.sparse
from matplotlib import pyplot as plt

import kernel_collection

modul = 2
# n_steps =0b1001001001001
n_steps = 103 * 32 + 27  # 41+13*13*29
kernel = np.array(kernel_collection.kernel)

datatype = np.uint8
worst_case_sum = modul * kernel.sum()
if worst_case_sum > 255:
    datatype = np.int16
if worst_case_sum > 32767:
    datatype = np.int32

print("using %s" % str(datatype))
state = np.ones((1, 1), dtype=datatype)
# state[1:-1,1:-1]=0

sparse_kernel = scipy.sparse.dok_matrix(kernel, dtype=datatype)


def make_sparse_base_fast(kernel, num):
    sparse_kernel = scipy.sparse.dok_matrix(kernel, dtype=datatype)
    shape = np.array(kernel.shape)
    base = []
    exp = 1
    for i in range(num):
        new_shape = (shape - (1, 1)) * (exp - 1) + shape
        new_kernel = scipy.sparse.dok_matrix(tuple(new_shape), dtype=datatype)
        for k in sparse_kernel.keys():
            new_kernel[k[0] * exp, k[1] * exp] = sparse_kernel[k]
            pass
        base.append(new_kernel)
        exp *= modul
    # for b in base: #watch out, the dense matrices get big very quick!
    #    print(b)
    #    plt.imshow(b.todense())
    #    plt.show()
    return base


sparse_base = make_sparse_base_fast(sparse_kernel, 1 + int(math.log(n_steps, modul)))


def sparse_step(state, sparse_kernel):
    new_shape = np.array(state.shape) + np.array(sparse_kernel.shape) - [1, 1]
    new_state = np.zeros(new_shape, dtype=datatype)

    state_shape = state.shape
    for k in sparse_kernel.keys():
        new_state[k[0]:k[0] + state_shape[0], k[1]:k[1] + state_shape[1]] += state
    new_state %= modul
    return new_state


print("ye")

name = str(n_steps)
c_fac = np.uint8(255 / (modul - 1))

print("\"performing\" %d iterations" % n_steps)

time_start = time.time()
i = 1
num = 0
while n_steps > 0:
    r = n_steps % modul
    print(num, r)

    for i in range(r):
        print("    ", state.shape, sparse_base[num].shape)
        state = sparse_step(state, sparse_base[num])

    num += 1
    n_steps = int(n_steps / modul)

    # imageio.imwrite("./intermediate_results/" + str(num) + ".png", state * c_fac)
    # plt.imshow(state,cmap="gray")
    # plt.show()

time_end = time.time()
print("done in %f seconds" % (time_end - time_start))

print("saving, final size:", state.shape)
time_start = time.time()
imageio.imwrite("./results_sparse_conv/" + str(name) + ".png", state * c_fac)
time_end = time.time()
print("seved in %f seconds" % (time_end - time_start))

plt.imshow(state)
plt.show()
