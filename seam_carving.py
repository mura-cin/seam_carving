import os
from time import time
import numpy as np
from skimage.io import imread, imsave
from calc_energy import calc_energy

def calc_M(E):
    rows, cols = E.shape
    M = np.array(E, copy=True)
    for y in range(1, rows):
        for x in range(cols):
            t = M[y-1,x]
            if x-1 >= 0:   t = min(t, M[y-1,x-1])
            if x+1 < cols: t = min(t, M[y-1,x+1])
            M[y,x] += t
    return M

def backtrack_M(M):
    rows, cols = M.shape
    seam_idx = np.zeros(rows, dtype=np.uint16)
    val = M[rows-1,0]
    for x in range(1, cols):
        if val > M[rows-1,x]:
            seam_idx[rows-1] = x
            val = M[rows-1,x]

    for y in reversed(range(rows-1)):
        idx = seam_idx[y+1]
        val = np.inf
        for x in range(idx-1, idx+2):
            if x < 0 or cols <= x: continue
            if val > M[y,x]:
                seam_idx[y] = x
                val = M[y,x]
    
    return seam_idx

def update(img, E, idx):
    rows, cols = E.shape
    u_img = np.zeros((rows, cols-1, 3), dtype=np.uint8)
    u_E  = np.zeros((rows, cols-1))
    for y in range(rows):
        if idx[y] == 0:
            u_img[y,:,:] = img[y,idx[y]+1:,:]
            u_E[y,:]    =  E[y,idx[y]+1:]
        elif idx[y] == cols-1:
            u_img[y,:,:] = img[y,:idx[y],:]
            u_E[y,:]    =  E[y,:idx[y]]
        else:
            u_img[y,:,:] = np.concatenate((img[y,:idx[y],:], img[y,idx[y]+1:,:]), axis=0)
            u_E[y,:]    = np.concatenate(( E[y,:idx[y]],    E[y,idx[y]+1:]),   axis=0)

    
    return u_img, u_E

def seam_carving(img, E, disp_time=False):
    if disp_time:
        s = time()
        M = calc_M(E)
        print('calc_M: {:.2f}s'.format(time()-s))
        
        s = time()
        idx = backtrack_M(M)
        print('backtrack_M: {:.2f}s'.format(time()-s))

        s = time()
        u = update(img, E, idx)
        print('update: {:.2f}s'.format(time()-s))
    else:
        M = calc_M(E)
        idx = backtrack_M(M)
        u = update(img, E, idx)

    return u

if __name__ == "__main__":
    img_path = 'path/to/img'
    img = imread(img_path)
    E = calc_energy(img).astype(np.float32)
    rows, cols = E.shape
    r_rows, r_cols = 800, 1000

    for i in range(cols-r_cols):
        print('i_x: {}/{}'.format(i+1, cols-r_cols))
        img, E = seam_carving(img, E, disp_time=True)
    
    img = img.transpose(1, 0, 2)
    E = E.transpose()
    for i in range(rows-r_rows):
        print('i_y: {}/{}'.format(i+1, rows-r_rows))
        img, E = seam_carving(img, E, disp_time=True)
    img = img.transpose(1, 0, 2)
    
    base_path, img_name = os.path.split(img_path)
    name, ext = os.path.splitext(img_name)
    imsave(os.path.join(base_path, name+'_resized'+ext), img)