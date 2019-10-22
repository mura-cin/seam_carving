import numpy as np
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