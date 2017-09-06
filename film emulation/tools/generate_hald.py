#!/usr/bin/env python3

import numpy as np
import skimage
import skimage.io

level=4  # hald4
# level=5  # hald5
# level=8  # hald8
cube_size=level*level
image_size=level*level*level
A=np.zeros(image_size*(image_size+2)*3)
i=0
for blue in range(0, cube_size):
    for green in range(0, cube_size):
        for red in range(0, cube_size):
             A[i]=float(red)/float(cube_size-1)
             i+=1
             A[i]=float(green)/float(cube_size-1)
             i+=1
             A[i]=float(blue)/float(cube_size-1)
             i+=1
for gray in range(0, 2*image_size):
    A[i]=float(gray)/float(2*image_size-1)
    i+=1
    A[i]=float(gray)/float(2*image_size-1)
    i+=1
    A[i]=float(gray)/float(2*image_size-1)
    i+=1

A=np.reshape(A, (image_size+2, image_size, 3))
skimage.io.imsave('hald{}.png'.format(level), A)
