import numpy as np
cimport numpy as cnp
cimport cython

@cython.wraparound(False)
@cython.boundscheck(False)
def calc_M(cnp.ndarray[cnp.float32_t, ndim=2] E):
    cdef:
        int rows, cols, x, y
        cnp.float32_t t
        cnp.ndarray[cnp.float32_t, ndim=2] M
    
    rows = E.shape[0]
    cols = E.shape[1]
    M = E.copy()
    for y in range(1, rows):
        for x in range(cols):
            t = M[y-1,x]
            if x-1 >= 0:   t = min(t, M[y-1,x-1])
            if x+1 < cols: t = min(t, M[y-1,x+1])
            M[y,x] += t
    return M