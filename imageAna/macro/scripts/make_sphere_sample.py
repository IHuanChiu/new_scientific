import numpy as np
from scipy import ndimage, misc

nvoxels=40
sample_array = np.zeros((nvoxels,nvoxels,nvoxels),dtype=float)

def sphere(shape, radius, position):
    # assume shape and position are both a 3-tuple of int or float
    # the units are pixels / voxels (px for short)
    # radius is a int or float in px
    semisizes = (radius,) * 3

    # genereate the grid for the support points
    # centered at the position indicated by position
    grid = [slice(-x0, dim - x0) for x0, dim in zip(position, shape)]
    position = np.ogrid[grid]
    # calculate the distance of all points from `position` center
    # scaled by the radius
    arr = np.zeros(shape, dtype=float)
    for x_i, semisize in zip(position, semisizes):
        # this can be generalized for exponent != 2
        # in which case `(x_i / semisize)`
        # would become `np.abs(x_i / semisize)`
        arr += (x_i / semisize) ** 2

    # the inner part of the sphere will have distance below 1
    return arr <= 1.0

if __name__ == '__main__':
   move=(10,10,5)
   _angle=10
   poi_big1=(0.0+move[0], 0.0+move[1], 0.0+6.35+move[2])
   np_sphereBig1=sphere((nvoxels,nvoxels,nvoxels),12.7/2,poi_big1)
   np_sphereBig2=sphere((nvoxels,nvoxels,nvoxels),12.7/2,(poi_big1[0]+6.351, poi_big1[1]+10.0+10, poi_big1[2]+3.175+6.35))
   np_sphereSamll1=sphere((nvoxels,nvoxels,nvoxels),12.7/4,(poi_big1[0]+10.51, poi_big1[1]+3.175, poi_big1[2]-6.35+6.35))
   np_sphereSmall2=sphere((nvoxels,nvoxels,nvoxels),12.7/4,(poi_big1[0]+6.0, poi_big1[1]-3.175+10, poi_big1[2]+10.5+6.35))
   sample_array=np_sphereBig1+np_sphereBig2+np_sphereSamll1+np_sphereSmall2
#   sample_array=ndimage.rotate(sample_array,_angle,axes=(0,2),reshape=False)
   with open('Sample_4sphere.npy', 'wb') as f:
      np.save(f, sample_array)
