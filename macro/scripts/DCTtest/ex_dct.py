#!/bin/env python
import numpy as np
import scipy.misc
from scipy.fftpack import dct, idct
import sys
import imageio
from skimage.transform import resize
from PIL import Image

H = 128
W = 128
lenna = resize(scipy.misc.ascent(), (H, W)).astype(np.float64)
lenna_F = dct(dct(lenna, axis=0), axis=1) ## 2D DCT of lenna

canvas = np.zeros((H,W))
for h in range(H):
    for w in range(W):
        a = np.zeros((H,W))
        a[h,w] = 100
        base = idct(idct(a, axis=0), axis=1) ## create dct bases
        canvas += lenna_F[h,w] * base ## accumulate
#    imageio.imwrite("base-%03d-%03d.png" % (h, w), base)
     imageio.imwrite("lenna-%03d-%03d.png" % (h, w), canvas)
